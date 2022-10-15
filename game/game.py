from flask import Blueprint, render_template


game_blueprint = Blueprint(
    name="game",
    template_folder="./templates",
    static_folder="static",
    static_url_path="/game/static",
    import_name=__name__
)


@game_blueprint.route("/game_bot", methods=["GET"])
def game_bot():
    return render_template("game/game.html")


@game_blueprint.route("/game_dealer", methods=["GET"])
def game_dealer():
    return render_template("game/game.html")
