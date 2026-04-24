from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.enums import AnalysisStatus


class AnalysisExecution(Base):
    __tablename__ = "analysis_executions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"), index=True)
    status: Mapped[AnalysisStatus] = mapped_column(Enum(AnalysisStatus), default=AnalysisStatus.pending, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    repository = relationship("Repository", back_populates="analyses")
    selected_policies = relationship(
        "AnalysisPolicySelection", back_populates="analysis_execution", cascade="all,delete-orphan"
    )
    policy_results = relationship("PolicyResult", back_populates="analysis_execution", cascade="all,delete-orphan")
    evidences = relationship("Evidence", back_populates="analysis_execution", cascade="all,delete-orphan")


class AnalysisPolicySelection(Base):
    __tablename__ = "analysis_policy_selections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    analysis_execution_id: Mapped[int] = mapped_column(ForeignKey("analysis_executions.id", ondelete="CASCADE"))
    policy_id: Mapped[int] = mapped_column(ForeignKey("policies.id"))

    analysis_execution = relationship("AnalysisExecution", back_populates="selected_policies")
    policy = relationship("Policy")
