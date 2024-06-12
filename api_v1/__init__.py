from fastapi import APIRouter

from .products.views import products_router

router_v1 = APIRouter()
router_v1.include_router(products_router, prefix="/products", tags=["Products"])
