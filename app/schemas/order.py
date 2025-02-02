from pydantic import BaseModel
from typing import Optional
from enum import Enum


# Enum for Order Status
class OrderStatusEnum(str, Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    FAILED = "Failed"


# Base schema for shared fields
class OrderBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float  # Change to float
    order_description: str
    status: str
    tracking_number: Optional[str] = None

    class Config:
        orm_mode = True  # Enable ORM mode


# Schema for creating a new order
class OrderCreate(OrderBase):
    user_id: str
    sellerId: str
    fulfillment_source_id: int
    fulfillment_source_type: str  # Either "seller" or "warehouse"
    is_backup_fulfillment: Optional[bool] = False  # Default to False
    owner_id: int 
    product_id: int
    quantity: int
    
# Schema for reading and displaying orders
class Order(OrderBase):
    id: int
    tracking_status: OrderStatusEnum
    tracking_info: Optional[str] = None  # Tracking info can be optional
    user_id: str
    sellerId: str
    fulfillment_source_id: int
    fulfillment_source_type: str
    is_backup_fulfillment: bool

    class Config:
        from_attributes = True


# Schema for updating an existing order
class OrderUpdate(BaseModel):
    quantity: Optional[int] = None
    total_price: Optional[float] = None
    tracking_status: Optional[OrderStatusEnum] = None
    tracking_info: Optional[str] = None
    owner_id: Optional[int] = None
    
    class Config:
        orm_mode = True

class OrderResponse(OrderBase):
    id: int
    owner_id: int
    quantity: int

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility

class OrderInDBBase(OrderBase):
    id: int
    user_id: str
    product_id: int

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility

class Order(OrderInDBBase):
    pass
