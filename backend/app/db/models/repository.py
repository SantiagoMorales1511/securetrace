from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.enums import RepositoryStatus


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    root_path: Mapped[str] = mapped_column(String(1024), unique=True, index=True)
    status: Mapped[RepositoryStatus] = mapped_column(Enum(RepositoryStatus), default=RepositoryStatus.loaded)
    loaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    artifacts = relationship("Artifact", back_populates="repository", cascade="all,delete-orphan")
    analyses = relationship("AnalysisExecution", back_populates="repository")
