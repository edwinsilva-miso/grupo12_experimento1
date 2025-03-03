from dotenv import load_dotenv
from flask import Flask

loaded = load_dotenv('.env.development')


from .blueprints.products_blueprint import products_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(products_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
