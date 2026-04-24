from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.policy import PolicyOut, RuleOut
from app.services.policy_service import PolicyService

router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("", response_model=list[PolicyOut])
def list_policies(db: Session = Depends(get_db)) -> list[PolicyOut]:
    service = PolicyService(db)
    return service.list_policies()


@router.get("/{policy_id}/rules", response_model=list[RuleOut])
def list_policy_rules(policy_id: int, db: Session = Depends(get_db)) -> list[RuleOut]:
    service = PolicyService(db)
    return service.list_policy_rules(policy_id)
