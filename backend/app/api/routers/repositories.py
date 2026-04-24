from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.repository import ArtifactListOut, ArtifactSummaryOut, LoadRepositoryRequest, RepositoryOut
from app.services.repository_service import RepositoryService

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.post("/load", response_model=RepositoryOut)
def load_repository(payload: LoadRepositoryRequest, db: Session = Depends(get_db)) -> RepositoryOut:
    service = RepositoryService(db)
    return service.load_repository(payload)


@router.get("/{repository_id}/artifacts", response_model=ArtifactListOut)
def list_artifacts(repository_id: int, db: Session = Depends(get_db)) -> ArtifactListOut:
    service = RepositoryService(db)
    return service.list_artifacts(repository_id)


@router.get("/{repository_id}/artifacts/summary", response_model=ArtifactSummaryOut)
def artifacts_summary(repository_id: int, db: Session = Depends(get_db)) -> ArtifactSummaryOut:
    service = RepositoryService(db)
    return service.artifacts_summary(repository_id)
