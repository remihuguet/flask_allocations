from flask import Flask
from . import services

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/products", methods=["GET"])
def list_products():
    return {
        "products": [
            {"sku": p.sku, "batches": p.batches} for p in services.list_products()
        ]
    }
