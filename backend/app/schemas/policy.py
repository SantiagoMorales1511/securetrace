from pydantic import BaseModel, ConfigDict


class RuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    policy_id: int
    code: str
    name: str
    description: str
    rule_type: str
    artifact_scope: str
    severity_default: str


class PolicyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    description: str
    category: str
    is_active: bool


class PolicyWithRulesOut(PolicyOut):
    rules: list[RuleOut]
