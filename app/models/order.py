from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database import BaseModel

class OrderModel(BaseModel):
    __tablename__ = "orders"
     
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)  # Removed ForeignKey constraint for now
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    order_date = Column(DateTime, nullable=False)
    tracking_status = Column(String, default="Pending")  # New column for tracking status
    tracking_info = Column(String, nullable=True)  # New column for tracking information
    user_id = Column(Integer, nullable=False)  # Removed ForeignKey constraint for now
    vendor_id = Column(Integer, nullable=False)  # Removed ForeignKey constraint for now
