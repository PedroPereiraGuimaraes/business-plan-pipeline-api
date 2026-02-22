from fastapi import APIRouter
from app.routers import auth as auth_router
from app.routers import projects as projects_router
from app.routers import onboarding as onboarding_router
from app.routers import plans as plans_router
from app.routers import consulting as consulting_router

api_router = APIRouter()

api_router.include_router(auth_router.router)
api_router.include_router(projects_router.router)
api_router.include_router(onboarding_router.router)
api_router.include_router(plans_router.router)
api_router.include_router(consulting_router.router)
