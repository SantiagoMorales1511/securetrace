from collections import defaultdict
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.analysis.rules.catalog import RuleRegistry
from app.db.models.analysis import AnalysisExecution, AnalysisPolicySelection
from app.db.models.artifact import Artifact
from app.db.models.enums import AnalysisStatus, EvidenceResult, PolicyComplianceStatus
from app.db.models.evidence import Evidence
from app.db.models.policy import Policy
from app.db.models.policy_result import PolicyResult
from app.db.models.repository import Repository
from app.db.models.rule import Rule


class AnalysisEngine:
    def __init__(self) -> None:
        self.registry = RuleRegistry()

    def run(self, db: Session, execution: AnalysisExecution) -> AnalysisExecution:
        execution.status = AnalysisStatus.running
        db.flush()

        repository = db.get(Repository, execution.repository_id)
        if repository is None:
            execution.status = AnalysisStatus.failed
            execution.finished_at = datetime.now(timezone.utc)
            db.flush()
            return execution

        artifacts = (
            db.query(Artifact)
            .filter(Artifact.repository_id == repository.id)
            .order_by(Artifact.relative_path.asc())
            .all()
        )

        selections = (
            db.query(AnalysisPolicySelection)
            .filter(AnalysisPolicySelection.analysis_execution_id == execution.id)
            .all()
        )

        policy_ids = [selection.policy_id for selection in selections]
        policies = db.query(Policy).filter(Policy.id.in_(policy_ids)).all() if policy_ids else []

        for policy in policies:
            self._run_policy(db=db, execution=execution, policy=policy, artifacts=artifacts, repository=repository)

        execution.status = AnalysisStatus.completed
        execution.finished_at = datetime.now(timezone.utc)
        db.flush()
        return execution

    def _run_policy(
        self,
        *,
        db: Session,
        execution: AnalysisExecution,
        policy: Policy,
        artifacts: list[Artifact],
        repository: Repository,
    ) -> None:
        rules = (
            db.query(Rule)
            .filter(Rule.policy_id == policy.id, Rule.is_active.is_(True))
            .order_by(Rule.id.asc())
            .all()
        )
        if not rules:
            db.add(
                PolicyResult(
                    analysis_execution_id=execution.id,
                    policy_id=policy.id,
                    status=PolicyComplianceStatus.requiere_revision,
                    summary="La politica no tiene reglas activas para evaluar",
                )
            )
            db.flush()
            return

        evidence_by_result: dict[EvidenceResult, int] = defaultdict(int)

        for rule in rules:
            evaluator = self.registry.get(rule.rule_type)
            if evaluator is None:
                evidence = Evidence(
                    analysis_execution_id=execution.id,
                    policy_id=policy.id,
                    rule_id=rule.id,
                    artifact_id=None,
                    result=EvidenceResult.error,
                    message=f"No hay evaluador para rule_type={rule.rule_type}",
                    snippet=None,
                )
                db.add(evidence)
                evidence_by_result[EvidenceResult.error] += 1
                continue

            evaluations = evaluator.evaluate(rule=rule, artifacts=artifacts, repository_root=repository.root_path)
            for item in evaluations:
                db.add(
                    Evidence(
                        analysis_execution_id=execution.id,
                        policy_id=policy.id,
                        rule_id=rule.id,
                        artifact_id=item.artifact_id,
                        result=item.result,
                        message=item.message,
                        snippet=item.snippet,
                    )
                )
                evidence_by_result[item.result] += 1

        status = self._policy_status_from_evidence(evidence_by_result)
        summary = self._build_summary(evidence_by_result)
        db.add(
            PolicyResult(
                analysis_execution_id=execution.id,
                policy_id=policy.id,
                status=status,
                summary=summary,
            )
        )
        db.flush()

    def _policy_status_from_evidence(
        self, evidence_by_result: dict[EvidenceResult, int]
    ) -> PolicyComplianceStatus:
        if evidence_by_result[EvidenceResult.failed] > 0:
            return PolicyComplianceStatus.no_cumple
        if evidence_by_result[EvidenceResult.error] > 0:
            return PolicyComplianceStatus.requiere_revision
        if evidence_by_result[EvidenceResult.review] > 0 and evidence_by_result[EvidenceResult.passed] == 0:
            return PolicyComplianceStatus.requiere_revision
        return PolicyComplianceStatus.cumple

    def _build_summary(self, evidence_by_result: dict[EvidenceResult, int]) -> str:
        return (
            f"pass={evidence_by_result[EvidenceResult.passed]}, "
            f"fail={evidence_by_result[EvidenceResult.failed]}, "
            f"review={evidence_by_result[EvidenceResult.review]}, "
            f"error={evidence_by_result[EvidenceResult.error]}"
        )
