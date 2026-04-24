from abc import ABC, abstractmethod
from typing import Any

from app.db.models.artifact import Artifact
from app.db.models.rule import Rule

from app.analysis.types import RuleEvaluationResult


class RuleEvaluator(ABC):
    @abstractmethod
    def evaluate(self, *, rule: Rule, artifacts: list[Artifact], repository_root: str) -> list[RuleEvaluationResult]:
        raise NotImplementedError

    def _parse_params(self, rule: Rule) -> dict[str, Any]:
        try:
            import json

            data = json.loads(rule.params_json or "{}")
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
