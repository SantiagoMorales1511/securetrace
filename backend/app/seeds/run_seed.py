from app.db.database import Base, SessionLocal, engine
from app.db.models import (  # noqa: F401
    AnalysisExecution,
    AnalysisPolicySelection,
    Artifact,
    Evidence,
    Policy,
    PolicyResult,
    Repository,
    Rule,
)
from app.seeds.policies_seed import seed_policies_and_rules


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_policies_and_rules(db)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
