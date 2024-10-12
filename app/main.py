from fastapi import FastAPI, Depends
from app.routes import order as order_route
from app.database import engine, BaseModel
from app.rabbitmq.order_created import RabbitMQClient

# Initialize FastAPI with metadata for Swagger
app = FastAPI(
    title="Order Service API",
    description=(
        "API documentation for the Order Service. "
        "This service manages customer orders, tracks order status, and publishes events to RabbitMQ."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "orders", "description": "Operations related to managing orders"},
    ],
)

# Initialize database tables
BaseModel.metadata.create_all(bind=engine)

# Initialize RabbitMQ client
rabbitmq_client = RabbitMQClient()

# Register the order router with RabbitMQ client as a dependency
app.include_router(order_route.router, prefix="/orders", tags=["orders"], dependencies=[Depends(lambda: rabbitmq_client)])

@app.get("/", tags=["root"])
def read_root():
    """
    Root endpoint that welcomes users to the Order Service API.
    """
    return {"message": "Welcome to the Order Service"}

# Shutdown RabbitMQ client when the application shuts down
@app.on_event("shutdown")
def shutdown_event():
    rabbitmq_client.close()
