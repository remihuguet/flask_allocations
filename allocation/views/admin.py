from flask import Blueprint, render_template
from allocation.repository import repository
from allocation import services


admin = Blueprint("admin", __name__)


@admin.route("/products", methods=["GET"])
def list_products():
    return render_template(
        "products_list.html", products=services.list_products(repository)
    )
