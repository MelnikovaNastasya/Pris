from fastapi import APIRouter

from . import customers, products, orders, analytics, dashboard

api_router = APIRouter()

api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(
    analytics.router, prefix="/analytics", tags=["analytics"]
)
api_router.include_router(dashboard.router, tags=["dashboard"])

