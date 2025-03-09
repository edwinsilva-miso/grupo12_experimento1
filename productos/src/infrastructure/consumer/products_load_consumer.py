import json
import logging
import os

import pika
from pika.exceptions import AMQPConnectionError

from ..adapter.product_adapter import ProductAdapter
from ..mapper.product_mapper import ProductMapper
from ...application.create_multiple_products import CreateMultipleProducts

RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
PRODUCTS_ROUTING_KEY = os.getenv('PRODUCTS_ROUTING_KEY')

logger = logging.getLogger(__name__)

class ProductsLoadConsumer:

    def __init__(self):
        self.adapter = ProductAdapter()
        self.mapper = ProductMapper()
        self.command = CreateMultipleProducts(self.adapter)
        self.connection = None
        self.channel = None

    def connect(self):
        logger.info(f"Connecting to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")

        # Setup connection parameters
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )

        # Connect to RabbitMQ server
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Declare queue (This ensure the queue exists)
        self.channel.queue_declare(queue=PRODUCTS_ROUTING_KEY, durable=True)

        logger.info(f"Connected to RabbitMQ, consuming from queue: {PRODUCTS_ROUTING_KEY}")

    def process_products(self, ch, method, properties, body):
        """
        Process incoming message from RabbitMQ

        Args:
            ch: Channel
            method: Method
            properties: Properties
            body: Message body
        """
        try:
            print(f'Received payload: {body}')

            # Transform the payload data to a list of DTOs
            products = self.mapper.from_json_to_dto_list(json.loads(body))

            # Execute the command
            self.command.execute(products)

            # Acknowledgement message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Successfully processed message")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON message: {body}")
            # Acknowledge invalid messages to avoid queue blocking
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            # Reject the message and requeue it
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


    def start(self):
        try:
            self.connect()

            self.channel.basic_consume(
                queue=PRODUCTS_ROUTING_KEY,
                on_message_callback=self.process_products)

            logging.debug("Starting to consume messages")
            self.channel.start_consuming()
        except AMQPConnectionError as e:
            logger.error(f"AMQP Connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in consumer: {str(e)}")
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            raise

    def stop(self):
        """Stop consuming messages and close connection"""
        if self.channel and self.channel.is_open:
            self.channel.stop_consuming()

        if self.connection and not self.connection.is_closed:
            self.connection.close()

        logger.info("Consumer stopped")




