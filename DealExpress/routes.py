from .forms import SignupForm
from flask import render_template, Blueprint, redirect, url_for
from .models import User
from DealExpress import db

from DealExpress.APIs.amazon import Amazon
from DealExpress.APIs.eBay import eBay
from DealExpress.APIs.rakuten import Rakuten
from DealExpress.APIs.target import Target
#from DealExpress import flaskObj

routes = Blueprint('routes', __name__)

@routes.route('/create-account', methods=['GET', 'POST'])
def createAccount():
    signUp = SignupForm()
    if signUp.validate_on_submit(): #button pressed, user filled all entries of form
        #check password match, valid email, user not exists
        #user_exists = User.query(email=signUp.email.data).first()
        user = User(email=signUp.email.data, name=signUp.name.data, password1=signUp.password1.data)#use password1 data from form, p2 would work too after our checks
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('routes.homePage'))
    return render_template("/signUp.html", title = 'Create Account', form=signUp)    

@routes.route('/', methods=["GET"])
def homePage():
    return render_template("Categories.html")

@routes.route('/product-search/', methods=["GET"])
def productSearchPage():
    return render_template("productSearch.html")

@routes.route('/subscription-pricing/', methods=["GET"])
def subscriptionPricingHome():
    return render_template("subscriptionPricing.html")

# Amazon Routes API
@routes.route('/product-search/api/amazon/<string:searchInput>/<string:pageID>', methods=["POST"])
def productResults(searchInput:str, pageID:int):
    return Amazon(searchInput).getProducts(pageID)

@routes.route('/product-search/api/amazon/bestsellers/', methods=["POST"])
def productSearchHomePageData():
    return Amazon(None).getBestSellerProducts()

@routes.route('/api/get-upc/<string:productASIN>', methods=["POST"])
def productUPC_API(productASIN:str):
    return Amazon(None).getProductUPC(productASIN)

# Target Routes API
@routes.route('/product-search/api/target/<string:UPC>/<string:amazonProductTitle>', methods=["POST"])
def targetProductLookUp(UPC:str, amazonProductTitle: str):
    return Target(amazonProductTitle).lookUpProduct_UPC(UPC)

# eBay Routes API
@routes.route('/product-search/api/ebay/<string:UPC>', methods=["POST"])
def eBayProductLookUp(UPC:str):
    return eBay(UPC).searchProduct()

# Rakuten Routes API
@routes.route("/api/rakuten/get-cashback/<string:retailer>", methods=["POST"])
def getRakutenCashback(retailer:str):
    return Rakuten(retailer).rakutenCashBack()
