from __future__ import annotations

from typing import Optional

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.enums import EvidenceResult


class Evidence(Base):
    __tablename__ = "evidences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    analysis_execution_id: Mapped[int] = mapped_column(ForeignKey("analysis_executions.id", ondelete="CASCADE"))
    policy_id: Mapped[int] = mapped_column(ForeignKey("policies.id"))
    rule_id: Mapped[int] = mapped_column(ForeignKey("rules.id"))
    artifact_id: Mapped[Optional[int]] = mapped_column(ForeignKey("artifacts.id"), nullable=True)
    result: Mapped[EvidenceResult] = mapped_column(Enum(EvidenceResult), index=True)
    message: Mapped[str] = mapped_column(Text)
    snippet: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    analysis_execution = relationship("AnalysisExecution", back_populates="evidences")
    policy = relationship("Policy", back_populates="evidences")
    rule = relationship("Rule", back_populates="evidences")
    artifact = relationship("Artifact", back_populates="evidences")
