from fastapi import APIRouter

router = APIRouter()

from .routers.products import router as products_router

router.include_router(products_router)