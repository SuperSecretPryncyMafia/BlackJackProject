from black_jack import BlackJack
from flask import redirect
from home.home import home_blueprint

app = BlackJack()


@app.route("/")
def from_root_to_home():
    return redirect("/home")


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'super secret key'
    app.register_blueprint(home_blueprint)
    app.run(debug=True)
