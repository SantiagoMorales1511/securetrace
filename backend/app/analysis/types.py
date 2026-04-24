from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.db.models.enums import EvidenceResult


@dataclass
class RuleEvaluationResult:
    result: EvidenceResult
    message: str
    artifact_id: Optional[int] = None
    snippet: Optional[str] = None
