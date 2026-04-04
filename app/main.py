from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import logger, settings
from app.core.database import Base, engine, get_db
from app.routes import geography, indicators, policies, sectors, tools

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(geography.router, prefix="/api/v1")
app.include_router(sectors.router, prefix="/api/v1")
app.include_router(indicators.router, prefix="/api/v1")
app.include_router(policies.router, prefix="/api/v1")
app.include_router(tools.router, prefix="/api/v1")

logger.info("BridgeStack %s started", settings.app_version)


@app.get("/", tags=["Health"])
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "stacks": {
            "data": "RootStack",
            "api": "BridgeStack",
            "frontend": "ViewStack",
            "analysis": "EquityStack",
            "fieldwork": "FieldStack",
            "mel": "InsightStack",
            "content": "SignalStack",
        },
    }


@app.get("/health", tags=["Health"])
def health_check():
    db = next(get_db())
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "unavailable"
        logger.warning("Health check: database unreachable")
    finally:
        db.close()

    status = "healthy" if db_status == "connected" else "degraded"
    return {
        "status": status,
        "version": settings.app_version,
        "database": db_status,
    }
