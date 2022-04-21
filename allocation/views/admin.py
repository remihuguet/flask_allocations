from flask import Blueprint, current_app, redirect, render_template, request, url_for
from allocation import services


admin = Blueprint("admin", __name__)


@admin.route("/products", methods=["GET"])
def list_products():
    return render_template(
        "products_list.html", products=services.list_products(current_app.repository)
    )


@admin.route("/products/add_batch", methods=["GET", "POST"])
def add_batch_form():
    if request.method == "GET":
        return render_template("add_batch.html")

    reference = request.form["reference"]
    qty = int(request.form["quantity"])
    sku = request.form["sku"]
    services.add_batch(
        reference=reference,
        sku=sku,
        quantity=qty,
        repository=current_app.repository,
        eta=None,
    )
    return render_template(
        "products_list.html",
        products=services.list_products(current_app.repository),
        message=f"Batch reference {reference} for {qty} of product {sku} created.",
    )


@admin.route("/products/allocate", methods=["GET", "POST"])
def allocate():
    if request.method == "GET":
        return render_template(
            "allocate.html",
            products=services.list_products(repository=current_app.repository),
        )

    orderid = request.form["orderid"]
    quantity = int(request.form["quantity"])
    sku = request.form["sku"]
    batchref = services.allocate(
        orderid=orderid, sku=sku, quantity=quantity, repository=current_app.repository
    )
    return render_template(
        "products_list.html",
        products=services.list_products(current_app.repository),
        message=f"Order id {orderid} for {quantity} of product {sku} allocated to batch {batchref}.",
    )
