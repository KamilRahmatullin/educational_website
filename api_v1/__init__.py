from fastapi import APIRouter

from .demo_auth.demo_jwt_auth import demo_jwt_auth_router
from .demo_auth.views import demo_auth_router
from .products.views import products_router

router_v1 = APIRouter()
router_v1.include_router(products_router, prefix='/products', tags=["Products"])
router_v1.include_router(demo_auth_router, prefix='/demo-auth', tags=["Demo Auth"])
router_v1.include_router(demo_jwt_auth_router, prefix='/demo-jwt-auth', tags=['Demo Jwt Auth'])
