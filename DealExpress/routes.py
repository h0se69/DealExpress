from flask import render_template
from DealExpress import flaskObj


@flaskObj.route('/', methods=["GET"])
def homePage():
    return render_template("home.html")