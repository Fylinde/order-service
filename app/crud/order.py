from sqlalchemy.orm import Session
from app.models.order import OrderModel
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.logistics_service import find_nearest_warehouse,check_warehouse_inventory
from app.services.collaboration_service import find_seller_collaborators, check_seller_inventory, SELLER_COLLABORATORS

# 1. Find the best fulfillment option (nearest warehouse or seller)
def find_best_fulfillment(db: Session, order: OrderCreate):
    """
    Finds the best fulfillment option for an order by checking the nearest sellers or warehouses.
    """
    # Step 1: Check the nearest warehouse with available stock
    nearest_warehouse = find_nearest_warehouse(order.buyer_location)
    if nearest_warehouse and check_warehouse_inventory(nearest_warehouse, order.product_id):
        return nearest_warehouse
    
    # Step 2: Check seller collaborators within proximity
    collaborators = find_seller_collaborators(order.seller_id)
    for seller in collaborators:
        if check_seller_inventory(seller, order.product_id):
            return seller

    return None

# 2. Fallback Fulfillment
def fallback_fulfillment(db: Session, order: OrderCreate):
    """
    Fallback logic to find an alternate seller or warehouse when the nearest one fails.
    Expands the search area and checks other warehouses or seller collaborators.
    """
    # Step 1: Try finding a farther warehouse with available stock
    farther_warehouses = find_nearest_warehouse(order.buyer_location, expand_search=True)
    for warehouse in farther_warehouses:
        if check_warehouse_inventory(warehouse, order.product_id):
            return warehouse

    # Step 2: Try to find alternate sellers through collaboration partners
    fallback_sellers = find_seller_collaborators(order.seller_id, expand_search=True)
    for seller in fallback_sellers:
        if check_seller_inventory(seller, order.product_id):
            return seller

    return None

# 3. Create Order and Assign Fulfillment Source
def create_order(db: Session, order: OrderCreate, fulfillment_source):
    """
    Create a new order and assign it to the selected fulfillment source (seller/warehouse).
    """
    new_order = OrderModel(
        buyer_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=order.total_price,  # Total price calculated earlier
        fulfillment_source_id=fulfillment_source.id,  # Fulfillment source (seller/warehouse)
        fulfillment_source_type=fulfillment_source.type,  # 'seller' or 'warehouse'
        tracking_status="created",
        tracking_info=None  # Tracking information can be updated later
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# 4. Get All Orders
def get_orders(db: Session):
    return db.query(OrderModel).all()

# 5. Get Order by ID
def get_order_by_id(db: Session, order_id: int):
    return db.query(OrderModel).filter(OrderModel.id == order_id).first()

# 6. Update Order
def update_order(db: Session, order_id: int, order_update: OrderUpdate):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if db_order is None:
        return None

    if order_update.quantity is not None:
        db_order.quantity = order_update.quantity

    if order_update.total_price is not None:
        db_order.total_price = order_update.total_price

    if order_update.tracking_status is not None:
        db_order.tracking_status = order_update.tracking_status

    if order_update.tracking_info is not None:
        db_order.tracking_info = order_update.tracking_info

    db.commit()
    db.refresh(db_order)
    return db_order

# 7. Delete Order
def delete_order(db: Session, order_id: int):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if db_order is None:
        return False
    db.delete(db_order)
    db.commit()
    return True

# 8. Get All Orders (for listing)
def get_all_orders(db: Session):
    return db.query(OrderModel).all()

# 9. Get a Specific Order by ID
def get_order(db: Session, order_id: int):
    return db.query(OrderModel).filter(OrderModel.id == order_id).first()

def get_orders_by_user(db: Session, user_id: int):
    return db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
