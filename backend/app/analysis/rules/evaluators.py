from pathlib import Path

from app.analysis.rules.base import RuleEvaluator
from app.analysis.types import RuleEvaluationResult
from app.db.models.artifact import Artifact
from app.db.models.enums import ArtifactType, EvidenceResult
from app.db.models.rule import Rule


class PatternMatchRuleEvaluator(RuleEvaluator):
    def evaluate(self, *, rule: Rule, artifacts: list[Artifact], repository_root: str) -> list[RuleEvaluationResult]:
        params = self._parse_params(rule)
        patterns = [p.lower() for p in params.get("patterns", []) if isinstance(p, str)]
        if not patterns:
            return [RuleEvaluationResult(result=EvidenceResult.review, message="Regla sin patrones configurados")]

        artifact_scope = params.get("artifact_scope", ["source", "config"])
        allowed = {ArtifactType(item) for item in artifact_scope if item in {t.value for t in ArtifactType}}

        findings: list[RuleEvaluationResult] = []
        scanned_any = False
        for artifact in artifacts:
            if artifact.artifact_type not in allowed:
                continue
            scanned_any = True
            absolute = Path(repository_root, artifact.relative_path)
            if not absolute.exists() or not absolute.is_file():
                continue
            try:
                content = absolute.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                findings.append(
                    RuleEvaluationResult(
                        result=EvidenceResult.error,
                        message=f"No fue posible leer {artifact.relative_path}",
                        artifact_id=artifact.id,
                    )
                )
                continue
            for pattern in patterns:
                if pattern in content:
                    findings.append(
                        RuleEvaluationResult(
                            result=EvidenceResult.failed,
                            message=f"Patron inseguro detectado: {pattern}",
                            artifact_id=artifact.id,
                            snippet=pattern,
                        )
                    )
        if findings:
            return findings
        if not scanned_any:
            return [RuleEvaluationResult(result=EvidenceResult.review, message="Sin artefactos aplicables para regla")]
        return [RuleEvaluationResult(result=EvidenceResult.passed, message="No se detectaron patrones inseguros")]


class DependencyPresenceRuleEvaluator(RuleEvaluator):
    def evaluate(self, *, rule: Rule, artifacts: list[Artifact], repository_root: str) -> list[RuleEvaluationResult]:
        params = self._parse_params(rule)
        tokens = [p.lower() for p in params.get("disallowed_tokens", []) if isinstance(p, str)]
        if not tokens:
            return [RuleEvaluationResult(result=EvidenceResult.review, message="Regla sin tokens de dependencia")]

        findings: list[RuleEvaluationResult] = []
        dependency_artifacts = [a for a in artifacts if a.artifact_type == ArtifactType.dependency]
        if not dependency_artifacts:
            return [RuleEvaluationResult(result=EvidenceResult.review, message="No hay artefactos de dependencias")]

        for artifact in dependency_artifacts:
            absolute = Path(repository_root, artifact.relative_path)
            if not absolute.exists() or not absolute.is_file():
                continue
            content = absolute.read_text(encoding="utf-8", errors="ignore").lower()
            for token in tokens:
                if token in content:
                    findings.append(
                        RuleEvaluationResult(
                            result=EvidenceResult.failed,
                            message=f"Dependencia o version sospechosa: {token}",
                            artifact_id=artifact.id,
                            snippet=token,
                        )
                    )
        if findings:
            return findings
        return [RuleEvaluationResult(result=EvidenceResult.passed, message="No se detectaron dependencias sospechosas")]


class ConfigFlagRuleEvaluator(RuleEvaluator):
    def evaluate(self, *, rule: Rule, artifacts: list[Artifact], repository_root: str) -> list[RuleEvaluationResult]:
        params = self._parse_params(rule)
        flags = [p.lower() for p in params.get("forbidden_flags", []) if isinstance(p, str)]
        if not flags:
            return [RuleEvaluationResult(result=EvidenceResult.review, message="Regla sin flags configuradas")]

        findings: list[RuleEvaluationResult] = []
        config_artifacts = [a for a in artifacts if a.artifact_type == ArtifactType.config]
        if not config_artifacts:
            return [RuleEvaluationResult(result=EvidenceResult.review, message="No hay artefactos de configuracion")]

        for artifact in config_artifacts:
            absolute = Path(repository_root, artifact.relative_path)
            if not absolute.exists() or not absolute.is_file():
                continue
            content = absolute.read_text(encoding="utf-8", errors="ignore").lower()
            for flag in flags:
                if flag in content:
                    findings.append(
                        RuleEvaluationResult(
                            result=EvidenceResult.failed,
                            message=f"Flag insegura detectada: {flag}",
                            artifact_id=artifact.id,
                            snippet=flag,
                        )
                    )
        if findings:
            return findings
        return [RuleEvaluationResult(result=EvidenceResult.passed, message="No se detectaron flags inseguras")]
