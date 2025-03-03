from flask import Blueprint, jsonify, request

from ..application.create_product import CreateProduct
from ..application.delete_product import DeleteProduct
from ..application.get_all_products import GetAllProducts
from ..application.get_product_by_id import GetProductById
from ..application.update_product import UpdateProduct
from ..domain.entities.product_dto import ProductDTO
from ..infrastructure.adapter.product_adapter import ProductAdapter

product_blueprint = Blueprint('products', __name__, url_prefix='/api/products')

product_adapter = ProductAdapter()


@product_blueprint.route('/', methods=['GET'])
def get_products():
    get_all_products = GetAllProducts(product_adapter)
    products = get_all_products.execute()
    return jsonify([product.__dict__ for product in products]), 200


@product_blueprint.route('/<string:product_id>', methods=['GET'])
def get_product(product_id: str):
    get_product_by_id = GetProductById(product_adapter)
    product = get_product_by_id.execute(product_id)
    if product is None:
        return {'message': 'Product not found'}, 404
    return jsonify(product.__dict__), 200


@product_blueprint.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    product = ProductDTO(
        id=None,
        name=data['name'],
        price=float(data['price'])
    )
    create_product = CreateProduct(product_adapter)
    product_id = create_product.execute(product)
    return jsonify({'id': product_id}), 201


@product_blueprint.route('/<string:product_id>', methods=['PUT'])
def update_product_route(product_id: str):
    data = request.get_json()
    product = ProductDTO(
        id=product_id,
        name=data['name'],
        price=float(data['price'])
    )
    update_product = UpdateProduct(product_adapter)
    updated_product = update_product.execute(product)
    if updated_product is None:
        return {'message': 'Product not found'}, 404
    return jsonify(updated_product.__dict__), 200


@product_blueprint.route('/<string:product_id>', methods=['DELETE'])
def delete_product_route(product_id: str):
    delete_product = DeleteProduct(product_adapter)
    delete_product.execute(product_id)
    return '', 204
