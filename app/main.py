import logging
import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command

from app.config import settings
from app.api import api_router

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run Alembic migrations programmatically."""
    try:
        # Assuming alembic.ini is in the root directory relative to where the app is run
        alembic_ini_path = "alembic.ini"
        if not os.path.exists(alembic_ini_path):
             # Fallback if running from a subdirectory, though standard is root
             alembic_ini_path = "../alembic.ini"

        if os.path.exists(alembic_ini_path):
            logger.info(f"Found alembic.ini at {alembic_ini_path}. Running migrations...")
            alembic_cfg = Config(alembic_ini_path)
            # Make sure to set the script location if it's relative in .ini
            # Usually alembic.ini has `script_location = alembic` so it should work 
            # if CWD is correct.
            command.upgrade(alembic_cfg, "head")
            logger.info("Migrations completed successfully.")
        else:
            logger.warning("alembic.ini not found. Skipping migrations.")
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        # Re-raise if you want the app to fail startup on migration failure
        # raise e

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run migrations
    logger.info("Starting up application...")
    # Run in a separate thread to not block the event loop
    # NOTE(User): Disable auto-migrations to prevent startup hang with remote DBs like Supabase
    # await asyncio.to_thread(run_migrations)
    yield
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    lifespan=lifespan
)

# CORS Configuration
origins = settings.BACKEND_CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"--> {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"<-- {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        raise e

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
    )

# Include the centralized API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Business Plan Pipeline API is running"}
