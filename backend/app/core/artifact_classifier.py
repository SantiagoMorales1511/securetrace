from pathlib import Path

from app.db.models.enums import ArtifactType

SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".rb",
    ".php",
    ".cs",
    ".cpp",
    ".c",
    ".rs",
}
CONFIG_EXTENSIONS = {".yaml", ".yml", ".json", ".ini", ".toml", ".env", ".xml", ".cfg", ".conf"}
DEPENDENCY_FILENAMES = {
    "requirements.txt",
    "poetry.lock",
    "pipfile",
    "pipfile.lock",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "pom.xml",
    "build.gradle",
    "go.mod",
    "go.sum",
    "cargo.toml",
    "cargo.lock",
}


def classify_artifact(path: Path) -> ArtifactType:
    filename = path.name.lower()
    extension = path.suffix.lower()

    if filename in DEPENDENCY_FILENAMES:
        return ArtifactType.dependency
    if extension in SOURCE_EXTENSIONS:
        return ArtifactType.source
    if extension in CONFIG_EXTENSIONS:
        return ArtifactType.config
    return ArtifactType.other
