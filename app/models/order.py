from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import BaseModel
import enum

class OrderStatusEnum(enum.Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    FAILED = "Failed"

class OrderModel(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    order_date = Column(DateTime, nullable=False)
    tracking_status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    tracking_info = Column(String, nullable=True)
    tracking_number = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    fulfillment_source_id = Column(Integer, nullable=False)
    fulfillment_source_type = Column(String, nullable=False)
    is_backup_fulfillment = Column(Integer, default=0)
    status = Column(String)
    
    # Relationships
    product = relationship("ProductModel", back_populates="orders")
    user = relationship("UserModel", back_populates="orders")
    vendor = relationship("VendorModel", back_populates="orders")
