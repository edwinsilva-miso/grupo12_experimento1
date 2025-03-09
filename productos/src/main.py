import threading
import logging
import time

from dotenv import load_dotenv
from flask import Flask

loaded = load_dotenv('.env.development')

from .infrastructure.database.declarative_base import Base, engine
from .interface.product_blueprint import product_blueprint
from .infrastructure.consumer.products_load_consumer import ProductsLoadConsumer

logging.basicConfig(level=logging.DEBUG)


def create_app():
    logging.debug("Start application")
    app = Flask(__name__)
    # Register blueprints
    app.register_blueprint(product_blueprint)

    # Create schema
    logging.debug(">> Create schema")
    Base.metadata.create_all(engine)

    thread = threading.Thread(target=start_consumer)
    thread.daemon = True
    thread.start()
    logging.debug("<< Consumer started")

    return app


def start_consumer():
    logging.debug("Consumer will start")
    # Start consuming messages
    consumer = ProductsLoadConsumer()
    # Retry connection to RabbitMQ if it fails
    max_retries = 5
    retry_delay = 5  # seconds
    for attempt in range(max_retries):
        try:
            consumer.start()
            break
        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            logging.info(f"Retrying in {retry_delay} seconds")
            time.sleep(retry_delay)


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
