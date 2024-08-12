from pydantic import BaseModel

class OrderBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float  # Change to float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    quantity: int
    total_price: float

    class Config:
        orm_mode = True