from flask import Blueprint, send_from_directory


home_blueprint = Blueprint(
    name="game",
    template_folder="./templates",
    import_name=__name__
)


@home_blueprint.route("/game", ["GET"])
def home():
    return send_from_directory("/html", "game.html")
