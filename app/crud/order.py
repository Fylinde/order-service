from sqlalchemy.orm import Session
from app.models import order as model_order
from app.schemas import order as schema_order

def create_order(db: Session, order: schema_order.OrderCreate):
    db_order = model_order.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
