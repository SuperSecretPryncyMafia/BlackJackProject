from flask import Blueprint, render_template


home_blueprint = Blueprint(
    name="game",
    template_folder="./templates",
    static_folder="static",
    static_url_path="/game/static",
    import_name=__name__
)


@home_blueprint.route("/game", ["GET"])
def home():
    return render_template("game/game.html")
