from __future__ import annotations

from typing import Optional

from app.analysis.rules.base import RuleEvaluator
from app.analysis.rules.evaluators import (
    ConfigFlagRuleEvaluator,
    DependencyPresenceRuleEvaluator,
    PatternMatchRuleEvaluator,
)


class RuleRegistry:
    def __init__(self) -> None:
        self._evaluators: dict[str, RuleEvaluator] = {
            "pattern_match_rule": PatternMatchRuleEvaluator(),
            "dependency_presence_rule": DependencyPresenceRuleEvaluator(),
            "config_flag_rule": ConfigFlagRuleEvaluator(),
        }

    def get(self, rule_type: str) -> Optional[RuleEvaluator]:
        return self._evaluators.get(rule_type)
