from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import Order, OrderCreate, OrderUpdate
from app.crud.order import create_order, get_orders, get_order_by_id, update_order, delete_order, get_all_orders, get_order
from typing import List

router = APIRouter()

@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order_route(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        db_order = create_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_order

@router.get("/", response_model=List[Order])
def read_orders(db: Session = Depends(get_db)):
    orders = get_orders(db)
    if not orders:
        return {"detail": "No orders found"}
    return orders

@router.get("/{order_id}", response_model=Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=Order)
def update_order_route(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = update_order(db, order_id, order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_route(order_id: int, db: Session = Depends(get_db)):
    result = delete_order(db, order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}

@router.get("/", response_model=List[Order], status_code=status.HTTP_200_OK)
def list_orders_route(db: Session = Depends(get_db)):
    orders = get_all_orders(db)
    return orders
