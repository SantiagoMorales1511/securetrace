from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.enums import ArtifactType


class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id", ondelete="CASCADE"), index=True)
    relative_path: Mapped[str] = mapped_column(String(1024), index=True)
    extension: Mapped[str] = mapped_column(String(20), default="")
    artifact_type: Mapped[ArtifactType] = mapped_column(Enum(ArtifactType), default=ArtifactType.other)
    size_bytes: Mapped[int] = mapped_column(default=0)

    repository = relationship("Repository", back_populates="artifacts")
    evidences = relationship("Evidence", back_populates="artifact")
