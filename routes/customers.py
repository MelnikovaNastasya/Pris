from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.Customer])
def list_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()


@router.post(
    "/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer_in: schemas.CustomerCreate, db: Session = Depends(get_db)
):
    customer = models.Customer(**customer_in.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

