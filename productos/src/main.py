import threading

from dotenv import load_dotenv
from flask import Flask

loaded = load_dotenv('.env.development')

from .infrastructure.database.declarative_base import Base, engine
from .interface.product_blueprint import product_blueprint
from .infrastructure.consumer.products_load_consumer import channel


def create_app():
    app = Flask(__name__)
    # Register blueprints
    app.register_blueprint(product_blueprint)

    # Create schema
    Base.metadata.create_all(engine)

    # Start consuming messages
    thread = threading.Thread(target=channel.start_consuming)
    thread.daemon = True
    thread.start()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
