from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.models.enums import AnalysisStatus, PolicyComplianceStatus


class AnalysisCreateRequest(BaseModel):
    repository_id: int
    policy_ids: list[int] = Field(min_length=1)

    @field_validator("policy_ids")
    @classmethod
    def validate_unique_ids(cls, values: list[int]) -> list[int]:
        if len(set(values)) != len(values):
            raise ValueError("policy_ids contiene duplicados")
        return values


class AnalysisExecutionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    repository_id: int
    status: AnalysisStatus
    started_at: datetime
    finished_at: Optional[datetime]


class PolicyResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    analysis_execution_id: int
    policy_id: int
    status: PolicyComplianceStatus
    score_optional: Optional[str]
    summary: str


class AnalysisResultsOut(BaseModel):
    analysis_execution_id: int
    results: list[PolicyResultOut]
