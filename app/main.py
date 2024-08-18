from fastapi import FastAPI
from app.routes import order as order_route
from app.database import engine, BaseModel

# Initialize FastAPI with metadata for Swagger
app = FastAPI(
    title="Order Service API",
    description="API documentation for the Order Service, which manages customer orders.",
    version="1.0.0",
    openapi_tags=[
        {"name": "orders", "description": "Operations related to managing orders"},
    ],
)

# Initialize database tables
BaseModel.metadata.create_all(bind=engine)

# Register the order router
app.include_router(order_route.router, prefix="/orders", tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Order Service"}
