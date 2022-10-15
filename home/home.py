
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
    if request.method == "GET":
        return render_template("home/home.html", home=background_process_test)
    elif request.method == "POST":
        return redirect("/game", home=background_process_test)


@home_blueprint.route('/background_process_test')
def background_process_test():
    print("Hello")
    return "nothing"
