from flask import Blueprint, render_template, jsonify
from .src.black_jack import Game


class GameBlueprint(Blueprint):
    def __init__(self):
        super().__init__(
            name="game",
            static_folder="static",
            template_folder="./templates",
            static_url_path="/game/static",
            url_prefix="/game",
            import_name=__name__
        )
        self.game = Game()

    def retrieve_one_card(self):
        return self.game.retrieve_one_card()


game_blueprint = GameBlueprint()


@game_blueprint.route("/game_bot", methods=["GET"])
def game_bot():
    return render_template("game/game.html")


@game_blueprint.route("/game_dealer", methods=["GET"])
def game_dealer():
    return render_template("game/game.html")


@game_blueprint.route("/game_dealer/deck", methods=["GET"])
def deck():
    return jsonify({"deck": game_blueprint.retrieve_one_card()})


@game_blueprint.route("/game_dealer/card", methods=["GET"])
def card():
    return jsonify(game_blueprint.retrieve_one_card())


@game_blueprint.route("/game_delaer/table", methods=["GET"])
def table():
    return jsonify(game_blueprint.game.retrieve_game())


@game_blueprint.route("/game_dealer/table_hit")
def table_hit():
    pass
