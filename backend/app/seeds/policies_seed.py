import json

from sqlalchemy.orm import Session

from app.db.models.policy import Policy
from app.db.models.rule import Rule


SEED_POLICIES = [
    {
        "code": "POL-SQLI-001",
        "name": "Prevencion de inyeccion SQL",
        "description": "Detecta patrones de concatenacion insegura en consultas SQL.",
        "category": "OWASP Top 10 - Injection",
        "rules": [
            {
                "code": "RULE-SQLI-RAW-QUERY",
                "name": "Consultas SQL inseguras",
                "description": "Busca patrones clasicos de SQL sin parametrizacion.",
                "rule_type": "pattern_match_rule",
                "artifact_scope": "source",
                "severity_default": "high",
                "params": {"patterns": ["select * from ", "execute(", "cursor.execute(f\""], "artifact_scope": ["source"]},
            }
        ],
    },
    {
        "code": "POL-XSS-001",
        "name": "Prevencion de XSS",
        "description": "Busca inserciones potencialmente inseguras en HTML/JS.",
        "category": "OWASP Top 10 - XSS",
        "rules": [
            {
                "code": "RULE-XSS-INNERHTML",
                "name": "Uso inseguro de innerHTML",
                "description": "Detecta uso de innerHTML/document.write.",
                "rule_type": "pattern_match_rule",
                "artifact_scope": "source",
                "severity_default": "high",
                "params": {"patterns": ["innerhtml", "document.write("], "artifact_scope": ["source"]},
            }
        ],
    },
    {
        "code": "POL-AUTH-001",
        "name": "Controles basicos de autenticacion",
        "description": "Valida configuraciones y patrones debiles de autenticacion.",
        "category": "OWASP ASVS - Authentication",
        "rules": [
            {
                "code": "RULE-AUTH-WEAK-SECRET",
                "name": "Secretos debiles por defecto",
                "description": "Detecta secretos hardcodeados comunes.",
                "rule_type": "pattern_match_rule",
                "artifact_scope": "config",
                "severity_default": "medium",
                "params": {
                    "patterns": ["secret=1234", "jwt_secret=changeme", "password=admin"],
                    "artifact_scope": ["source", "config"],
                },
            }
        ],
    },
    {
        "code": "POL-DATA-001",
        "name": "Manejo seguro de datos",
        "description": "Evalua banderas inseguras de configuracion relacionadas con proteccion de datos.",
        "category": "ISO 27001 - Data Protection",
        "rules": [
            {
                "code": "RULE-DATA-INSECURE-FLAGS",
                "name": "Flags de seguridad desactivadas",
                "description": "Busca DEBUG=true y disabled ssl verify.",
                "rule_type": "config_flag_rule",
                "artifact_scope": "config",
                "severity_default": "medium",
                "params": {"forbidden_flags": ["debug=true", "verify=false", "ssl_verify=false"]},
            }
        ],
    },
    {
        "code": "POL-DEP-001",
        "name": "Dependencias vulnerables",
        "description": "Detecta dependencias potencialmente riesgosas en manifest/lock files.",
        "category": "DevSecOps - Supply Chain",
        "rules": [
            {
                "code": "RULE-DEP-SUSPECT",
                "name": "Dependencias sospechosas",
                "description": "Busca tokens de versiones o paquetes inseguros predefinidos.",
                "rule_type": "dependency_presence_rule",
                "artifact_scope": "dependency",
                "severity_default": "high",
                "params": {"disallowed_tokens": ["log4j:2.14.1", "lodash@4.17.19", "pyyaml==5.3"]},
            }
        ],
    },
]


def seed_policies_and_rules(db: Session) -> None:
    for policy_seed in SEED_POLICIES:
        policy = db.query(Policy).filter(Policy.code == policy_seed["code"]).first()
        if policy is None:
            policy = Policy(
                code=policy_seed["code"],
                name=policy_seed["name"],
                description=policy_seed["description"],
                category=policy_seed["category"],
                is_active=True,
            )
            db.add(policy)
            db.flush()

        for rule_seed in policy_seed["rules"]:
            existing_rule = db.query(Rule).filter(Rule.code == rule_seed["code"]).first()
            if existing_rule is not None:
                continue
            db.add(
                Rule(
                    policy_id=policy.id,
                    code=rule_seed["code"],
                    name=rule_seed["name"],
                    description=rule_seed["description"],
                    rule_type=rule_seed["rule_type"],
                    artifact_scope=rule_seed["artifact_scope"],
                    severity_default=rule_seed["severity_default"],
                    params_json=json.dumps(rule_seed["params"], ensure_ascii=True),
                    is_active=True,
                )
            )
    db.flush()
