from flask import Flask, request, jsonify
from flask_validator import Validator
from werkzeug.exceptions import HTTPException


class ProductValidator(Validator):
    name = {"required": True, "type": str}
    price = {"required": True, "type": float}


app = Flask(__name__)

products = [
    {"id": 1, "name": "Product 1", "price": 10.00},
    {"id": 2, "name": "Product 2", "price": 20.00},
    {"id": 3, "name": "Product 3", "price": 30.00},
]


# GET /products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


# GET /products/:id
@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    try:
        product = next((product for product in products if product["id"] == id), None)
        if product is None:
            raise HTTPException(404)
        return jsonify(product)
    except HTTPException as e:
        return jsonify({"message": e.description}), e.code


# POST /products
jwt = JWTManager(app)


@app.route("/products", methods=["POST"])
@jwt_required
def create_product():
    product = request.json
    product["id"] = len(products) + 1
    products.append(product)
    return jsonify(product), 201


# PUT /products/:id
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = next((product for product in products if product["id"] == id), None)
    if product is None:
        return jsonify({"message": "Product not found."}), 404
    product.update(request.json)
    return jsonify(product)


# DELETE /products/:id
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = next((product for product in products if product["id"] == id), None)
    if product is None:
        return jsonify({"message": "Product not found."}), 404
    products.remove(product)
    return jsonify({}), 204


if __name__ == "__main__":
    app.run(debug=True)
