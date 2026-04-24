from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.policy import Policy
from app.db.models.rule import Rule


class PolicyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active_policies(self) -> list[Policy]:
        return (
            self.db.query(Policy)
            .filter(Policy.is_active.is_(True))
            .order_by(Policy.id.asc())
            .all()
        )

    def get_policy(self, policy_id: int) -> Optional[Policy]:
        return self.db.get(Policy, policy_id)

    def list_active_rules_by_policy(self, policy_id: int) -> list[Rule]:
        return (
            self.db.query(Rule)
            .filter(Rule.policy_id == policy_id, Rule.is_active.is_(True))
            .order_by(Rule.id.asc())
            .all()
        )
