from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.enums import ArtifactType, RepositoryStatus


class LoadRepositoryRequest(BaseModel):
    root_path: str = Field(min_length=1)


class RepositoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    root_path: str
    status: RepositoryStatus
    loaded_at: datetime


class ArtifactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    repository_id: int
    relative_path: str
    extension: str
    artifact_type: ArtifactType
    size_bytes: int


class ArtifactListOut(BaseModel):
    repository_id: int
    total: int
    artifacts: list[ArtifactOut]


class ArtifactSummaryItem(BaseModel):
    artifact_type: ArtifactType
    count: int


class ArtifactSummaryOut(BaseModel):
    repository_id: int
    summary: list[ArtifactSummaryItem]
