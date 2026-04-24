from __future__ import annotations

from typing import Optional

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.enums import PolicyComplianceStatus


class PolicyResult(Base):
    __tablename__ = "policy_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    analysis_execution_id: Mapped[int] = mapped_column(ForeignKey("analysis_executions.id", ondelete="CASCADE"))
    policy_id: Mapped[int] = mapped_column(ForeignKey("policies.id"))
    status: Mapped[PolicyComplianceStatus] = mapped_column(Enum(PolicyComplianceStatus), index=True)
    score_optional: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    summary: Mapped[str] = mapped_column(Text, default="")

    analysis_execution = relationship("AnalysisExecution", back_populates="policy_results")
    policy = relationship("Policy", back_populates="policy_results")
