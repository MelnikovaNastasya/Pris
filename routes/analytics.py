from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter()


@router.get("/popular-products", response_model=list[schemas.PopularProduct])
def popular_products(limit: int = 5, db: Session = Depends(get_db)):
    """
    Top-selling products by quantity.
    """
    rows = (
        db.query(
            models.Product.id.label("product_id"),
            models.Product.name.label("name"),
            func.sum(models.OrderItem.quantity).label("total_quantity"),
        )
        .join(models.OrderItem, models.OrderItem.product_id == models.Product.id)
        .group_by(models.Product.id, models.Product.name)
        .order_by(func.sum(models.OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )
    return [
        schemas.PopularProduct(
            product_id=row.product_id,
            name=row.name,
            total_quantity=row.total_quantity or 0,
        )
        for row in rows
    ]


@router.get("/revenue", response_model=schemas.RevenueSummary)
def revenue(db: Session = Depends(get_db)):
    """
    Total revenue across all orders.
    """
    total = db.query(func.coalesce(func.sum(models.Order.total_price), 0.0)).scalar()
    return schemas.RevenueSummary(total_revenue=float(total or 0.0))


@router.get(
    "/customer-stats", response_model=list[schemas.CustomerStats]
)
def customer_stats(limit: int = 5, db: Session = Depends(get_db)):
    """
    Most active customers by number of orders and total spent.
    """
    rows = (
        db.query(
            models.Customer.id.label("customer_id"),
            models.Customer.name.label("name"),
            func.count(models.Order.id).label("orders_count"),
            func.coalesce(func.sum(models.Order.total_price), 0.0).label(
                "total_spent"
            ),
        )
        .join(models.Order, models.Order.customer_id == models.Customer.id)
        .group_by(models.Customer.id, models.Customer.name)
        .order_by(
            func.count(models.Order.id).desc(),
            func.sum(models.Order.total_price).desc(),
        )
        .limit(limit)
        .all()
    )
    return [
        schemas.CustomerStats(
            customer_id=row.customer_id,
            name=row.name,
            orders_count=row.orders_count,
            total_spent=float(row.total_spent or 0.0),
        )
        for row in rows
    ]

