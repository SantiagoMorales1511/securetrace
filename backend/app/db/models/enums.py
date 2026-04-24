from enum import Enum


class ArtifactType(str, Enum):
    source = "source"
    config = "config"
    dependency = "dependency"
    other = "other"


class RepositoryStatus(str, Enum):
    loaded = "loaded"
    invalid = "invalid"


class AnalysisStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class PolicyComplianceStatus(str, Enum):
    cumple = "cumple"
    no_cumple = "no_cumple"
    requiere_revision = "requiere_revision"


class EvidenceResult(str, Enum):
    passed = "pass"
    failed = "fail"
    review = "review"
    error = "error"
