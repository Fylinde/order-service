from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import Order, OrderCreate, OrderUpdate
from app.crud.order import (
    create_order, get_orders, get_order_by_id, update_order, 
    delete_order, find_best_fulfillment, fallback_fulfillment, get_all_orders, get_order
)
from typing import List
from app.rabbitmq.order_created import RabbitMQClient
router = APIRouter()


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED, tags=["orders"])
def create_order_route(order: OrderCreate, db: Session = Depends(get_db), rabbitmq_client: RabbitMQClient = Depends()):
    try:
        # Step 1: Try to fulfill the order using the best possible seller or warehouse
        best_fulfillment = find_best_fulfillment(db, order)
        if best_fulfillment:
            db_order = create_order(db, order, best_fulfillment)
        else:
            # Step 2: If best fulfillment fails, attempt fallback
            fallback = fallback_fulfillment(db, order)
            if fallback:
                db_order = create_order(db, order, fallback)
            else:
                raise ValueError("No suitable seller or warehouse found to fulfill the order.")

        # Step 3: Publish order creation to RabbitMQ
        rabbitmq_client.publish_order_created(order.dict())

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return db_order

@router.get("/", response_model=List[Order], tags=["orders"])
def read_orders(db: Session = Depends(get_db)):
    """
    Retrieve all orders from the database.
    """
    orders = get_orders(db)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders

@router.get("/{order_id}", response_model=Order, tags=["orders"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an order by its ID.
    """
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=Order, tags=["orders"])
def update_order_route(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    """
    Update an existing order by its ID.
    """
    db_order = update_order(db, order_id, order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["orders"])
def delete_order_route(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order by its ID.
    """
    result = delete_order(db, order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}

# 6. List all orders (consolidated to avoid redundancy)
@router.get("/list", response_model=List[Order], status_code=status.HTTP_200_OK)
def list_orders_route(db: Session = Depends(get_db)):
    orders = get_orders(db)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders
@router.get("/orders/{user_id}", response_model=List[order_schema.Order])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    return order_crud.get_orders_by_user_id(db=db, user_id=user_id)
