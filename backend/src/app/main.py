import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from src.app.auth import get_current_admin_user, get_current_user
from src.app.routers.auth import router as auth_router
from src.app.routers.chat import router as chat_router
from src.app.routers.conversations import router as conversations_router
from src.app.routers.nhanh import router as nhanh_router
from src.app.routers.files import router as files_router
from src.app.routers.users import router as users_router
from src.commons.logger import configure_logging
from src.configs import SETTINGS

configure_logging()

logger.add(
    "logs/api_server.log",
    rotation="100 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    backtrace=True,
    diagnose=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Starlink Backend...")

    # Create tables if they don't exist
    from src.db.database import engine
    from sqlmodel import SQLModel
    import src.db.models.users  # noqa: F401
    import src.db.models.conversations  # noqa: F401
    import src.db.models.nhanh  # noqa: F401
    import src.db.models.files  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Seed demo user
    from src.db.database import get_manual_db_session
    from src.db.repositories.user import UserRepository
    from src.app.security import hash_password

    async with get_manual_db_session() as session:
        repo = UserRepository(session)
        existing = await repo.get_by_email("demo@starlink.chat")
        if not existing:
            await repo.create(
                email="demo@starlink.chat",
                name="Demo User",
                hashed_password=hash_password("password"),
                role="admin",
            )
            logger.info("Demo user created: demo@starlink.chat")

    yield
    logger.info("Shutting down Starlink Backend...")


# Ensure data directories exist for static file mounts
Path("data/generated_boms").mkdir(parents=True, exist_ok=True)
Path("data/uploads").mkdir(parents=True, exist_ok=True)
Path("data/managed_files").mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Starlink Backend", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in SETTINGS.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"{request.method} {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


# Public routes
app.include_router(
    auth_router,
    prefix="/api",
    tags=["auth"],
)

# Nhanh.vn integration routes (public - OAuth callback must be accessible)
app.include_router(
    nhanh_router,
    prefix="/api",
    tags=["nhanh"],
)

# Authenticated routes
app.include_router(
    conversations_router,
    prefix="/api",
    tags=["conversations"],
    dependencies=[Depends(get_current_user)],
)

app.include_router(
    chat_router,
    prefix="/api",
    tags=["chat"],
    dependencies=[Depends(get_current_user)],
)

# Admin-only routes
app.include_router(
    users_router,
    prefix="/api",
    tags=["users"],
    dependencies=[Depends(get_current_admin_user)],
)

app.include_router(
    files_router,
    prefix="/api",
    tags=["file-manager"],
    dependencies=[Depends(get_current_admin_user)],
)


# Static file serving for generated BOMs
app.mount(
    "/api/files/boms",
    StaticFiles(directory="data/generated_boms"),
    name="bom_files",
)

# Static file serving for uploaded images
app.mount(
    "/api/files/uploads",
    StaticFiles(directory="data/uploads"),
    name="upload_files",
)

# Static file serving for product datasheet images
app.mount(
    "/api/files/datasheets",
    StaticFiles(directory=SETTINGS.datasheets_dir),
    name="datasheet_files",
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "starlink-backend"}
