from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.core.config import get_settings
from app.db.base import Base  
from app.db.session import engine
from app.routers import attendance, dashboard, employee
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)



def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title=settings.PROJECT_NAME)

    
    if settings.BACKEND_CORS_ORIGINS:
        origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    else:
        
        origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        
        allow_origins=[
            "http://localhost:5173", "https://hrms-lite-1.netlify.app/"          ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    app.include_router(employee.router, prefix=settings.API_V1_PREFIX)
    app.include_router(attendance.router, prefix=settings.API_V1_PREFIX)
    app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)


    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

        inspector = inspect(engine)
        try:
            cols = {c["name"] for c in inspector.get_columns("employees")}
        except Exception:
            cols = set()

        if "deleted_at" not in cols:
            with engine.begin() as conn:
                conn.execute(
                    text("ALTER TABLE employees ADD COLUMN deleted_at TIMESTAMP")
                )

    return app


app = create_app()

