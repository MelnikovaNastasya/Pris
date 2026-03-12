from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.Product])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.post(
    "/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED
)
def create_product(
    product_in: schemas.ProductCreate, db: Session = Depends(get_db)
):
    product = models.Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

