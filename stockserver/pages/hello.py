from flask import Blueprint, render_template, abort

gretting_page = Blueprint("hello_page", __name__, template_folder="templates")

@gretting_page.route("/hello", defaults={"name": "user"})
@gretting_page.route("/hello/<name>")
def gretting(name):
    try:
        return render_template("test.html", name=name)
    except:
        abort(404)