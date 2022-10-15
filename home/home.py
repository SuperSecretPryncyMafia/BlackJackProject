
from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)


home_blueprint = Blueprint(
    name="home",
    template_folder="./templates",
    static_folder="static",
    static_url_path="/home/static",
    import_name=__name__
)


@home_blueprint.route("/home")
def home():
    if request.method == "POST":
        if request.form["start_button"] == "dealer":
            return redirect("/game", messages={"oponent": "dealer"})
        elif request.form["start_button"] == "bot":
            return redirect("/game", messages={"oponent": "bot"})
    elif request.method == "GET":
        return render_template("home/home.html")
