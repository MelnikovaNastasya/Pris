from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator

DATABASE_URL = "sqlite:///./retailgenie.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Create tables and insert simple seed data for demo purposes.
    """
    import models  # local import to avoid circulars

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # If there are already customers, assume DB is seeded
        if db.query(models.Customer).first():
            return

        # Seed customers
        alice = models.Customer(name="Alice Johnson", age=32, gender="female")
        bob = models.Customer(name="Bob Smith", age=45, gender="male")
        carol = models.Customer(name="Carol Lee", age=28, gender="female")

        db.add_all([alice, bob, carol])
        db.flush()

        # Seed products
        milk = models.Product(name="Organic Milk 1L", category="Dairy", price=2.99)
        bread = models.Product(name="Wholegrain Bread", category="Bakery", price=3.49)
        apples = models.Product(name="Red Apples 1kg", category="Fruit", price=4.29)
        cereal = models.Product(name="Breakfast Cereal", category="Grocery", price=5.99)

        db.add_all([milk, bread, apples, cereal])
        db.flush()

        # Seed orders and items
        from datetime import datetime, timedelta

        today = datetime.utcnow().date()

        order1 = models.Order(
            customer_id=alice.id,
            date=today - timedelta(days=2),
            total_price=0.0,
        )
        order2 = models.Order(
            customer_id=bob.id,
            date=today - timedelta(days=1),
            total_price=0.0,
        )
        order3 = models.Order(
            customer_id=alice.id,
            date=today,
            total_price=0.0,
        )

        db.add_all([order1, order2, order3])
        db.flush()

        items = [
            models.OrderItem(order_id=order1.id, product_id=milk.id, quantity=2),
            models.OrderItem(order_id=order1.id, product_id=bread.id, quantity=1),
            models.OrderItem(order_id=order2.id, product_id=apples.id, quantity=3),
            models.OrderItem(order_id=order2.id, product_id=milk.id, quantity=1),
            models.OrderItem(order_id=order3.id, product_id=cereal.id, quantity=2),
            models.OrderItem(order_id=order3.id, product_id=apples.id, quantity=1),
        ]
        db.add_all(items)
        db.flush()

        # Calculate order totals
        for order in (order1, order2, order3):
            total = 0.0
            for item in order.items:
                total += item.quantity * item.product.price
            order.total_price = total

        db.commit()
    finally:
        db.close()

