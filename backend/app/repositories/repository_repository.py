from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.artifact import Artifact
from app.db.models.repository import Repository


class RepositoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, repository_id: int) -> Optional[Repository]:
        return self.db.get(Repository, repository_id)

    def get_by_root_path(self, root_path: str) -> Optional[Repository]:
        return self.db.query(Repository).filter(Repository.root_path == root_path).first()

    def save_repository(self, repository: Repository) -> Repository:
        self.db.add(repository)
        self.db.flush()
        self.db.refresh(repository)
        return repository

    def replace_artifacts(self, repository_id: int, artifacts: list[Artifact]) -> None:
        self.db.query(Artifact).filter(Artifact.repository_id == repository_id).delete(synchronize_session=False)
        if artifacts:
            self.db.add_all(artifacts)
        self.db.flush()

    def list_artifacts(self, repository_id: int) -> list[Artifact]:
        return (
            self.db.query(Artifact)
            .filter(Artifact.repository_id == repository_id)
            .order_by(Artifact.relative_path.asc())
            .all()
        )
