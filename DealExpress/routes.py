from flask import render_template, Blueprint
#from DealExpress import flaskObj

routes = Blueprint('routes', __name__)

@routes.route('/', methods=["GET"])
def homePage():
    return render_template("home.html")