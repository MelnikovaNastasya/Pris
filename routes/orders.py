from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Order])
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@router.post(
    "/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED
)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Ensure customer exists
    customer = db.query(models.Customer).get(order_in.customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer does not exist.",
        )

    # Ensure all products exist
    product_ids = {item.product_id for item in order_in.items}
    products = (
        db.query(models.Product)
        .filter(models.Product.id.in_(product_ids))
        .all()
    )
    if len(products) != len(product_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more products do not exist.",
        )

    products_by_id = {p.id: p for p in products}

    order = models.Order(
        customer_id=order_in.customer_id,
        date=order_in.date or date.today(),
        total_price=0.0,
    )
    db.add(order)
    db.flush()

    total = 0.0
    for item_in in order_in.items:
        product = products_by_id[item_in.product_id]
        line_total = product.price * item_in.quantity
        total += line_total
        db_item = models.OrderItem(
            order_id=order.id,
            product_id=item_in.product_id,
            quantity=item_in.quantity,
        )
        db.add(db_item)

    order.total_price = total
    db.commit()
    db.refresh(order)
    return order

