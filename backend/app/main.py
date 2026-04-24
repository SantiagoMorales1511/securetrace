from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
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

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            seed_policies_and_rules(db)
            db.commit()
        finally:
            db.close()

    app.include_router(api_router, prefix="/api")
    return app


app = create_app()
