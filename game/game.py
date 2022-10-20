from flask import Blueprint, render_template, jsonify
from .src.black_jack import Game


class GameBlueprint(Blueprint, Game):
    def __init__(self):
        super().__init__(
            name="game",
            static_folder="static",
            template_folder="./templates",
            static_url_path="/game/static",
            url_prefix="/game",
            import_name=__name__
        )


game_blueprint = GameBlueprint()


@game_blueprint.route("/game_bot", methods=["GET"])
def game_bot():
    return render_template("game/game.html")


@game_blueprint.route("/game_dealer", methods=["GET"])
def game_dealer():
    return render_template("game/game.html")


@game_blueprint.route("/game_dealer/deck", methods=["GET"])
def deck():
    return jsonify(game_blueprint.post_one_card())


@game_blueprint.route("/game_dealer/card", methods=["GET"])
def card():
    return jsonify(game_blueprint.post_one_card())
