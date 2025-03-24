from fastapi import APIRouter

from src.api.v1.router import router as v1_router

main_router = APIRouter()
main_router.include_router(v1_router, prefix="/v1")
