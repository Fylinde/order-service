import pika
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# RabbitMQ connection parameters from environment variables
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'order_created')


class RabbitMQClient:
    def __init__(self):
        """
        Initialize RabbitMQ connection and channel.
        """
        try:
            # Establish RabbitMQ connection
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
            )
            self.channel = self.connection.channel()

            # Declare the queue to ensure it exists
            self.channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
            logging.info(f"Connected to RabbitMQ and declared queue '{RABBITMQ_QUEUE}'")

        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None

    def publish_order_created(self, order_data):
        """
        Publish a message to the RabbitMQ queue when an order is created.

        :param order_data: A dictionary with the order information.
        """
        if not self.connection or self.connection.is_closed:
            logging.error("No active RabbitMQ connection. Cannot publish message.")
            return

        try:
            # Serialize the order data to JSON
            message = json.dumps(order_data)

            # Publish the message to the queue
            self.channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_QUEUE,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )

            logging.info(f"Published message to queue '{RABBITMQ_QUEUE}': {message}")

        except Exception as e:
            logging.error(f"Error publishing message to RabbitMQ: {e}")

    def close(self):
        """
        Close the RabbitMQ connection.
        """
        if self.connection and self.connection.is_open:
            self.connection.close()
            logging.info("RabbitMQ connection closed.")


# Usage Example
if __name__ == "__main__":
    # Initialize the RabbitMQ client
    rabbitmq_client = RabbitMQClient()

    # Example order data
    order_data = {
        "order_id": 1234,
        "product_id": 5678,
        "quantity": 2,
        "total_price": 49.99,
        "user_id": 7890
    }

    # Publish an order created event
    rabbitmq_client.publish_order_created(order_data)

    # Close the connection when done
    rabbitmq_client.close()
