from flask import (
    Blueprint,
    render_template,
    jsonify
)
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

    def stay_or_hit_remote(self, decision: int):
        self.game.decision_made = decision

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


@game_blueprint.route("/game_dealer/table", methods=["GET"])
def table():
    return jsonify(game_blueprint.game.retrieve_game(["a"], [1, 10]))


@game_blueprint.route("/game_dealer/table_hit", method=["POST"])
def table_hit():
    game_blueprint.game.decision_made = 2


@game_blueprint.route("/game_dealer/table_stand", method=["POST"])
def table_stand():
    game_blueprint.game.decision_made = 1


@game_blueprint.route("/game_dealer/start_game")
def table_start():
    game_blueprint.game.remote_black_jack()
