from flask import Blueprint, request, send_from_directory


home_blueprint = Blueprint(name="home", import_name=__name__)

@home_blueprint.route("/home", ["GET"])
def home():
    return send_from_directory("/html", "home.html")