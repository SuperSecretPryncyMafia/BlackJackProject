from flask import Blueprint, render_template


game_blueprint = Blueprint(
    name="game",
    static_folder="static",
    static_url_path="/static",
    import_name=__name__
)


@game_blueprint.route("/game_bot", methods=["GET"])
def game_bot():
    return render_template("index.html")


@game_blueprint.route("/game_dealer", methods=["GET"])
def game_dealer():
    return render_template("index.html")
