import threading
import logging

from dotenv import load_dotenv
from flask import Flask

loaded = load_dotenv('.env.development')

from .infrastructure.database.declarative_base import Base, engine
from .interface.product_blueprint import product_blueprint
from .infrastructure.consumer.products_load_consumer import start_consumer

logging.basicConfig(level=logging.DEBUG)


def create_app():
    logging.debug("Start application")
    app = Flask(__name__)
    # Register blueprints
    app.register_blueprint(product_blueprint)

    # Create schema
    logging.debug(">> Create schema")
    Base.metadata.create_all(engine)

    logging.debug(">> Consumer will start")
    # Start consuming messages
    thread = threading.Thread(target=start_consumer)
    thread.daemon = True
    thread.start()
    logging.debug("<< Consumer started")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
