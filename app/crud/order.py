from sqlalchemy.orm import Session
from app.models.order import OrderModel
from app.schemas.order import OrderCreate, OrderUpdate
import requests

def create_order(db: Session, order: OrderCreate):
    # Validate product_id by calling product service
    response = requests.get(f"http://product-service:8003/products/{order.product_id}")
    if response.status_code != 200:
        raise ValueError("Invalid product_id")

    db_order = OrderModel(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session):
    return db.query(OrderModel).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(OrderModel).filter(OrderModel.id == order_id).first()

def update_order(db: Session, order_id: int, order_update: OrderUpdate):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if db_order is None:
        return None

    db_order.quantity = order_update.quantity
    db_order.total_price = order_update.total_price
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if db_order is None:
        return False
    db.delete(db_order)
    db.commit()
    return True

def get_all_orders(db: Session):
    return db.query(OrderModel).all()

def get_order(db: Session, order_id: int):
    return db.query(OrderModel).filter(OrderModel.id == order_id).first()

