from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.policy_repository import PolicyRepository
from app.schemas.policy import PolicyOut, RuleOut


class PolicyService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.policy_repo = PolicyRepository(db)

    def list_policies(self) -> list[PolicyOut]:
        policies = self.policy_repo.list_active_policies()
        return [PolicyOut.model_validate(policy) for policy in policies]

    def list_policy_rules(self, policy_id: int) -> list[RuleOut]:
        policy = self.policy_repo.get_policy(policy_id)
        if policy is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Politica no encontrada")
        rules = self.policy_repo.list_active_rules_by_policy(policy_id)
        return [RuleOut.model_validate(rule) for rule in rules]
