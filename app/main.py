from fastapi import FastAPI
from app.routes import order as order_route
from app.database import engine, BaseModel

app = FastAPI()

# Initialize database tables
BaseModel.metadata.create_all(bind=engine)

app.include_router(order_route.router, prefix="/orders", tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Order Service"}
