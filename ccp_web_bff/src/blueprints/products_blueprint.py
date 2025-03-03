from flask import request, Blueprint, jsonify

from ..commands.process_file import ProcessFile

products_blueprint = Blueprint('products', __name__, url_prefix='/bff/products')

@products_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        result = ProcessFile().execute(file)
        return jsonify(result), 200
    else:
        return jsonify({"message": "Invalid file format"}), 400

