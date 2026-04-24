from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.analysis import AnalysisCreateRequest, AnalysisExecutionOut, AnalysisResultsOut
from app.schemas.evidence import EvidenceListOut
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=AnalysisExecutionOut)
def create_analysis(payload: AnalysisCreateRequest, db: Session = Depends(get_db)) -> AnalysisExecutionOut:
    service = AnalysisService(db)
    return service.create_execution(payload)


@router.post("/{execution_id}/run", response_model=AnalysisExecutionOut)
def run_analysis(execution_id: int, db: Session = Depends(get_db)) -> AnalysisExecutionOut:
    service = AnalysisService(db)
    return service.run_execution(execution_id)


@router.get("/{execution_id}/results", response_model=AnalysisResultsOut)
def analysis_results(execution_id: int, db: Session = Depends(get_db)) -> AnalysisResultsOut:
    service = AnalysisService(db)
    return service.list_results(execution_id)


@router.get("/{execution_id}/evidence", response_model=EvidenceListOut)
def analysis_evidence(execution_id: int, db: Session = Depends(get_db)) -> EvidenceListOut:
    service = AnalysisService(db)
    return service.list_evidence(execution_id)
