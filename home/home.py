
from flask import (
    Blueprint,
    render_template,
    request
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
    if request.method == "GET":
        return render_template("home/home.html")
