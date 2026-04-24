from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.analysis import AnalysisExecution, AnalysisPolicySelection
from app.db.models.evidence import Evidence
from app.db.models.policy_result import PolicyResult


class AnalysisRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_execution(self, repository_id: int, policy_ids: list[int]) -> AnalysisExecution:
        execution = AnalysisExecution(repository_id=repository_id)
        self.db.add(execution)
        self.db.flush()

        selections = [
            AnalysisPolicySelection(analysis_execution_id=execution.id, policy_id=policy_id)
            for policy_id in policy_ids
        ]
        self.db.add_all(selections)
        self.db.flush()
        self.db.refresh(execution)
        return execution

    def get_execution(self, execution_id: int) -> Optional[AnalysisExecution]:
        return self.db.get(AnalysisExecution, execution_id)

    def list_results(self, execution_id: int) -> list[PolicyResult]:
        return (
            self.db.query(PolicyResult)
            .filter(PolicyResult.analysis_execution_id == execution_id)
            .order_by(PolicyResult.policy_id.asc())
            .all()
        )

    def list_evidence(self, execution_id: int) -> list[Evidence]:
        return (
            self.db.query(Evidence)
            .filter(Evidence.analysis_execution_id == execution_id)
            .order_by(Evidence.id.asc())
            .all()
        )
