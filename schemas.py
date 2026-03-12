from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    name: str
    age: int
    gender: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str
    category: str
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    customer_id: int
    date: date


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class PopularProduct(BaseModel):
    product_id: int
    name: str
    total_quantity: int


class RevenueSummary(BaseModel):
    total_revenue: float


class CustomerStats(BaseModel):
    customer_id: int
    name: str
    orders_count: int
    total_spent: float

