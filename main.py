from django.shortcuts import redirect
from flask import url_for
from black_jack import BlackJack

app = BlackJack()

@app.route("/", ["GET"])
def from_root_to_home():
    return redirect(url_for("/home"))
