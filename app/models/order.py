from sqlalchemy import Column, Integer, String
from app.database import BaseModel

class OrderModel(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    quantity = Column(Integer)
