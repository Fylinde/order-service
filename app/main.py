from fastapi import FastAPI
from app.database import engine
from app.models.order import OrderModel
from app.routes import order as order_route

app = FastAPI()

OrderModel.metadata.create_all(bind=engine)

app.include_router(order_route.router)
