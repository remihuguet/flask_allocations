from flask import Flask, render_template, request
from allocation import repository
from allocation.views.api import api
from allocation.views.admin import admin


def create_app(repository_class):

    app = Flask(__name__)

    app.repository = repository.initialize_repository(repository_class)

    app.register_blueprint(api)
    app.register_blueprint(admin, url_prefix="/admin")

    @app.route("/", methods=["GET"])
    def hello_world():
        name = request.args.get("name", "World")
        return render_template("index.html", name=name)

    return app
