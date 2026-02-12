from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.base import Base  # noqa: F401
from app.db.session import engine
from app.routers import attendance, dashboard, employee
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)



def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title=settings.PROJECT_NAME)

    # CORS
    if settings.BACKEND_CORS_ORIGINS:
        origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    else:
        # Development-friendly default: allow all
        origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(employee.router, prefix=settings.API_V1_PREFIX)
    app.include_router(attendance.router, prefix=settings.API_V1_PREFIX)
    app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)

    # Create tables on startup (simple, suitable for small apps)
    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()

