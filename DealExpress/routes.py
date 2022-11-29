from flask import render_template, Blueprint, redirect, url_for, flash
from DealExpress import db
from DealExpress.models import User
from flask_login import login_user

from DealExpress.APIs.amazon import Amazon
from DealExpress.APIs.eBay import eBay
from DealExpress.APIs.rakuten import Rakuten
from DealExpress.APIs.target import Target
#from DealExpress import flaskObj
from DealExpress.forms import SearchForm, SignupForm, LoginForm

routes = Blueprint('routes', __name__)

@routes.route('/', methods=["GET"])
def homePage():
#<<<<<<< Updated upstream
    return render_template("home.html")
#=======
    return render_template("home.html")