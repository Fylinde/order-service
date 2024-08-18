
### `API_DOCS.md`

```markdown
Order Service API Documentation

Overview
API documentation for the Order Service, which manages customer orders.

Version: 1.0.0
API Specification: OpenAPI 3.1

Endpoints

Order Management Endpoints

List Orders
- URL: /orders/
- Method: GET
- Summary: Retrieve a list of all customer orders.
- Response:
  - 200 Successful Response:
    {
      "type": "array",
      "items": {
        "$ref": "#/components/schemas/Order"
      }
    }

Create Order
- URL: /orders/
- Method: POST
- Summary: Create a new order for a product.
- Request Body:
  {
    "$ref": "#/components/schemas/OrderCreate"
  }
- Response:
  - 201 Successful Response:
    {
      "$ref": "#/components/schemas/Order"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Read Order
- URL: /orders/{order_id}
- Method: GET
- Summary: Retrieve details of a specific order by its ID.
- Parameters:
  - order_id (integer): The ID of the order.
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/Order"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Update Order
- URL: /orders/{order_id}
- Method: PUT
- Summary: Update the details of an existing order.
- Parameters:
  - order_id (integer): The ID of the order to update.
- Request Body:
  {
    "$ref": "#/components/schemas/OrderUpdate"
  }
- Response:
  - 200 Successful Response:
    {
      "$ref": "#/components/schemas/Order"
    }
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Delete Order
- URL: /orders/{order_id}
- Method: DELETE
- Summary: Remove an order from the system by its ID.
- Parameters:
  - order_id (integer): The ID of the order to delete.
- Response:
  - 204 Successful Response
  - 422 Validation Error:
    {
      "$ref": "#/components/schemas/HTTPValidationError"
    }

Miscellaneous Endpoints

Read Root
- URL: /
- Method: GET
- Summary: Root endpoint.
- Response:
  - 200 Successful Response:
    {}
