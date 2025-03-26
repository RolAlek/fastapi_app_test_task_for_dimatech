from fastapi import APIRouter

from src.api.handlers.authentication.router import router as auth_router
from src.api.handlers.transaction.router import router as transaction_router
from src.api.handlers.user.router import router as user_router

router = APIRouter()

router.include_router(router=auth_router, prefix="/auth", tags=["Auth"])
router.include_router(router=user_router, prefix="/users", tags=["Users"])
router.include_router(
    router=transaction_router,
    prefix="/transactions",
    tags=["Transactions"],
)
