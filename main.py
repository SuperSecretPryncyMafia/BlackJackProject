from black_jack import BlackJack
from flask import redirect, send_from_directory
from home.home import home_blueprint
from game.game import game_blueprint
app = BlackJack()


@app.route("/")
def from_root_to_home():
    return redirect("/home")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("./", "favicon.ico")


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'super secret key'
    app.register_blueprint(home_blueprint)
    app.register_blueprint(game_blueprint, url_prefix='/')
    app.run(debug=True)
