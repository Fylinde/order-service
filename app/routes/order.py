from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import order as crud_order
from app.schemas import order as schema_order

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders/", response_model=schema_order.Order)
def create_order(order: schema_order.OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create_order(db=db, order=order)
