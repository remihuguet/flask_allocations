from flask import Flask, jsonify, request

from allocation.repository import Repository
from . import services

app = Flask(__name__)

repository = Repository(products=[])


@app.route("/", methods=["GET"])
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/products", methods=["GET"])
def list_products():
    products = services.list_products(repository)

    products_as_dict = [
        {
            "sku": product.sku,
            "batches": [
                {
                    "reference": batch.reference,
                    "purchased_quantity": batch.purchased_quantity,
                    "available_quantity": batch.available_quantity,
                    "eta": batch.eta,
                    "allocated": [
                        {
                            "orderid": alloc.orderid,
                            "quantity": alloc.quantity,
                        }
                        for alloc in batch._allocated
                    ],
                }
                for batch in product.batches
            ],
        }
        for product in products
    ]
    return jsonify({"products": products_as_dict})


@app.route("/products/add_batch", methods=["POST"])
def add_batch():
    try:
        reference = request.json["reference"]
        sku = request.json["sku"]
        quantity = int(request.json["quantity"])
        eta = request.json["eta"] if "eta" in request.json else None
    except (KeyError, ValueError):
        return jsonify({"error": "Missing required field"}), 400

    services.add_batch(reference, sku, quantity, eta, repository)
    return jsonify({"status": "OK"}), 201
