from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.db.models.enums import EvidenceResult


class EvidenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    analysis_execution_id: int
    policy_id: int
    rule_id: int
    artifact_id: Optional[int]
    result: EvidenceResult
    message: str
    snippet: Optional[str]


class EvidenceListOut(BaseModel):
    analysis_execution_id: int
    evidence: list[EvidenceOut]
