from fastapi import APIRouter

from src.api.handlers.user.router import router as user_router

router = APIRouter()

router.include_router(router=user_router, prefix="/users", tags=["Users"])
