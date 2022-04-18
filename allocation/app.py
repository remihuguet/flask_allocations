from flask import Flask, render_template, request
from allocation.views.api import api
from allocation.views.admin import admin

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    name = request.args.get("name", "World")
    return render_template("index.html", name=name)


app.register_blueprint(api)
app.register_blueprint(admin, url_prefix="/admin")
