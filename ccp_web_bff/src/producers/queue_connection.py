import os
import logging

import pika

connection = None

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)

def get_connection():
    logging.debug("Getting connection")
    rabbitmq_user = os.getenv('RABBITMQ_USER')
    rabbitmq_password = os.getenv('RABBITMQ_PASSWORD')
    rabbitmq_host = os.getenv('RABBITMQ_HOST')
    rabbitmq_port = os.getenv('RABBITMQ_PORT')

    global connection
    if connection is None or connection.is_closed:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
            )
        )
    return connection
