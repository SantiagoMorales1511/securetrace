from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.analysis.engine import AnalysisEngine
from app.db.models.enums import AnalysisStatus
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.policy_repository import PolicyRepository
from app.repositories.repository_repository import RepositoryRepository
from app.schemas.analysis import AnalysisCreateRequest, AnalysisExecutionOut, AnalysisResultsOut, PolicyResultOut
from app.schemas.evidence import EvidenceListOut, EvidenceOut


class AnalysisService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.analysis_repo = AnalysisRepository(db)
        self.policy_repo = PolicyRepository(db)
        self.repository_repo = RepositoryRepository(db)
        self.engine = AnalysisEngine()

    def create_execution(self, payload: AnalysisCreateRequest) -> AnalysisExecutionOut:
        repository = self.repository_repo.get_by_id(payload.repository_id)
        if repository is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repositorio no encontrado")
        for policy_id in payload.policy_ids:
            if self.policy_repo.get_policy(policy_id) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Politica no encontrada: {policy_id}",
                )

        execution = self.analysis_repo.create_execution(
            repository_id=payload.repository_id,
            policy_ids=payload.policy_ids,
        )
        self.db.commit()
        self.db.refresh(execution)
        return AnalysisExecutionOut.model_validate(execution)

    def run_execution(self, execution_id: int) -> AnalysisExecutionOut:
        execution = self.analysis_repo.get_execution(execution_id)
        if execution is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ejecucion no encontrada")
        if execution.status == AnalysisStatus.running:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La ejecucion ya esta en curso")

        execution = self.engine.run(self.db, execution)
        self.db.commit()
        self.db.refresh(execution)
        return AnalysisExecutionOut.model_validate(execution)

    def list_results(self, execution_id: int) -> AnalysisResultsOut:
        execution = self.analysis_repo.get_execution(execution_id)
        if execution is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ejecucion no encontrada")
        results = self.analysis_repo.list_results(execution_id)
        return AnalysisResultsOut(
            analysis_execution_id=execution_id,
            results=[PolicyResultOut.model_validate(result) for result in results],
        )

    def list_evidence(self, execution_id: int) -> EvidenceListOut:
        execution = self.analysis_repo.get_execution(execution_id)
        if execution is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ejecucion no encontrada")
        evidence = self.analysis_repo.list_evidence(execution_id)
        return EvidenceListOut(
            analysis_execution_id=execution_id,
            evidence=[EvidenceOut.model_validate(item) for item in evidence],
        )
