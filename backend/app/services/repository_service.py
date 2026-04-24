from collections import Counter
import hashlib
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.artifact_classifier import classify_artifact
from app.core.config import get_settings
from app.db.models.artifact import Artifact
from app.db.models.enums import ArtifactType, RepositoryStatus
from app.db.models.repository import Repository
from app.repositories.repository_repository import RepositoryRepository
from app.schemas.repository import (
    ArtifactListOut,
    ArtifactSummaryItem,
    ArtifactSummaryOut,
    LoadRepositoryRequest,
    RepositoryOut,
)


class RepositoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository_repo = RepositoryRepository(db)
        self.settings = get_settings()

    def load_repository(self, payload: LoadRepositoryRequest) -> RepositoryOut:
        root = self._resolve_repository_path(payload.root_path)

        existing = self.repository_repo.get_by_root_path(str(root))
        repository = existing or Repository(name=root.name, root_path=str(root), status=RepositoryStatus.loaded)
        repository = self.repository_repo.save_repository(repository)

        artifacts = self._scan_artifacts(repository.id, root)
        self.repository_repo.replace_artifacts(repository.id, artifacts)
        self.db.commit()
        self.db.refresh(repository)
        return RepositoryOut.model_validate(repository)

    def _resolve_repository_path(self, source: str) -> Path:
        candidate = Path(source).expanduser().resolve()
        if candidate.exists() and candidate.is_dir():
            return candidate
        if self._looks_like_git_url(source):
            return self._clone_public_repository(source)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Entrada invalida. Usa ruta local existente o URL git publica",
        )

    def _looks_like_git_url(self, source: str) -> bool:
        if source.startswith("git@"):
            return True
        parsed = urlparse(source)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return source.endswith(".git") or "github.com" in parsed.netloc or "gitlab.com" in parsed.netloc
        return False

    def _clone_public_repository(self, url: str) -> Path:
        clone_base = Path(self.settings.repository_clone_dir).expanduser().resolve()
        clone_base.mkdir(parents=True, exist_ok=True)

        safe_name = re.sub(r"[^a-zA-Z0-9._-]+", "-", Path(url.rstrip("/")).stem) or "repo"
        suffix = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
        target = clone_base / f"{safe_name}-{suffix}"

        if target.exists() and (target / ".git").exists():
            return target

        if target.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ruta de cache de repositorio en conflicto",
            )

        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", url, str(target)],
                check=True,
                capture_output=True,
                text=True,
                timeout=self.settings.git_clone_timeout_sec,
            )
        except subprocess.TimeoutExpired as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Timeout al clonar repositorio remoto",
            ) from exc
        except subprocess.CalledProcessError as exc:
            message = exc.stderr.strip() or "No fue posible clonar el repositorio remoto"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message) from exc

        return target

    def list_artifacts(self, repository_id: int) -> ArtifactListOut:
        repository = self.repository_repo.get_by_id(repository_id)
        if repository is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repositorio no encontrado")

        artifacts = self.repository_repo.list_artifacts(repository_id)
        return ArtifactListOut(repository_id=repository_id, total=len(artifacts), artifacts=artifacts)

    def artifacts_summary(self, repository_id: int) -> ArtifactSummaryOut:
        repository = self.repository_repo.get_by_id(repository_id)
        if repository is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repositorio no encontrado")
        artifacts = self.repository_repo.list_artifacts(repository_id)
        counter = Counter([artifact.artifact_type for artifact in artifacts])
        summary = [ArtifactSummaryItem(artifact_type=artifact_type, count=count) for artifact_type, count in counter.items()]
        summary.sort(key=lambda item: item.artifact_type.value)
        return ArtifactSummaryOut(repository_id=repository_id, summary=summary)

    def _scan_artifacts(self, repository_id: int, root: Path) -> list[Artifact]:
        excluded = set(self.settings.repository_excluded_dirs)
        artifacts: list[Artifact] = []

        for path in root.rglob("*"):
            if path.is_dir():
                continue
            if any(part in excluded for part in path.parts):
                continue
            relative = path.relative_to(root).as_posix()
            extension = path.suffix.lower()
            artifact_type: ArtifactType = classify_artifact(path)
            artifacts.append(
                Artifact(
                    repository_id=repository_id,
                    relative_path=relative,
                    extension=extension,
                    artifact_type=artifact_type,
                    size_bytes=path.stat().st_size,
                )
            )
        return artifacts
