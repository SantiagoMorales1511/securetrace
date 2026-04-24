from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    policy_id: Mapped[int] = mapped_column(ForeignKey("policies.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    rule_type: Mapped[str] = mapped_column(String(80), index=True)
    artifact_scope: Mapped[str] = mapped_column(String(30), default="all")
    severity_default: Mapped[str] = mapped_column(String(20), default="medium")
    params_json: Mapped[str] = mapped_column(Text, default="{}")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    policy = relationship("Policy", back_populates="rules")
    evidences = relationship("Evidence", back_populates="rule")
