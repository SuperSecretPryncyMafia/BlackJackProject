from flask import redirect
from flask import Blueprint, jsonify, render_template

from .src.black_jack import ClassicBlackJack, NeuralBlackJack


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
        self.game = None
        self.frontend = {}

    def spawn_bot_game(self):
        self.game = ClassicBlackJack()
        self.game.spawn_decision_thread()

    def spawn_neural_game(self):
        self.game = NeuralBlackJack()

    def start_game(self):
        self.game.prepare_game()
        self.game.update_frontend()

    def stay_or_hit_remote(self, decision: int):
        self.game.player_decision = decision

    def retrieve_one_card(self):
        return self.game.retrieve_one_card()


game_blueprint = GameBlueprint()


@game_blueprint.route("/exit", methods=["GET"])
def game_end():
    game_blueprint.game = None
    game_blueprint.front_end = {}
    return redirect("/home")


@game_blueprint.route("/game_bot", methods=["GET"])
def game_bot():
    game_blueprint.spawn_neural_game()
    game_blueprint.start_game()
    return render_template("game/game.html")


@game_blueprint.route("/game_dealer", methods=["GET"])
def game_dealer():
    game_blueprint.spawn_bot_game()
    game_blueprint.start_game()
    return render_template("game/game.html")


@game_blueprint.route("/game_dealer/deck", methods=["GET"])
def deck():
    return jsonify({"deck": game_blueprint.retrieve_one_card()})


@game_blueprint.route("/game_dealer/card", methods=["GET"])
def card():
    return jsonify(game_blueprint.retrieve_one_card())


@game_blueprint.route("/game_dealer/table", methods=["GET"])
def table():
    return jsonify(game_blueprint.game.retrieve_game())


@game_blueprint.route("/game_dealer/table_hit")
def table_hit():
    game_blueprint.stay_or_hit_remote(1)
    return jsonify(game_blueprint.game.stay_or_hit_remote())


@game_blueprint.route("/game_dealer/table_stay")
def table_stay():
    game_blueprint.stay_or_hit_remote(0)
    return jsonify(game_blueprint.game.stay_or_hit_remote())


@game_blueprint.route("/game_dealer/round")
def round():
    game_blueprint.game.tour()
    return "200"
