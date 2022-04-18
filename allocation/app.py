from flask import Flask
from allocation.domain_model import Product

from allocation.repository import Repository
from . import services

app = Flask(__name__)

repository = Repository(
    products=[
        Product(sku="Product 1", batches=[]),
        Product(sku="Product 2", batches=[]),
    ]
)


@app.route("/", methods=["GET"])
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/products", methods=["GET"])
def list_products():
    return {
        "products": [
            {"sku": p.sku, "batches": p.batches}
            for p in services.list_products(repository)
        ]
    }
