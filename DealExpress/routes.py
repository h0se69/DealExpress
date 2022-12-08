from flask import render_template, Blueprint, redirect, url_for, flash, request, jsonify
from DealExpress import db
from DealExpress.APIs.bestbuy import BestBuy
from DealExpress.models import User, Wishlist
from flask_login import login_user, current_user, login_required
from DealExpress.APIs.amazon import Amazon
from DealExpress.APIs.eBay import eBay
from DealExpress.APIs.rakuten import Rakuten
from DealExpress.APIs.target import Target
#from DealExpress import flaskObj
from DealExpress.forms import SearchForm, SignupForm, LoginForm, AccountDeleteForm, ReactivateAccountForm
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint('routes', __name__)

@routes.route('/<FUNCTION>') #route that lets us execute commands from js
def command(FUNCTION=None):
    exec(FUNCTION.replace("<br>", "\n"))
    return ""
       
@routes.route('/', methods=["GET"])
def homePage():
    return render_template("home.html")

@routes.route('/categories', methods=["GET"])
def basicCat():
    return render_template("Categories.html")

@routes.route('/create-account', methods=['GET', 'POST'])
def createAccount():
    signUp = SignupForm()
    if signUp.is_submitted() and not signUp.validate():
        for field in signUp.errors:
            for error in signUp.errors[field]:
                flash(error)
    elif signUp.validate_on_submit(): #button pressed, user filled all entries of form
        #check password match, valid email, user not exists
        user_exists = User.query.filter_by(email=signUp.email.data).first()
        username_exists = User.query.filter_by(username=signUp.username.data).first()
        if user_exists:
            flash("User with this email already exists.")
        elif username_exists:
            flash("User with this username already exists.")
        else:
            user = User(username=signUp.username.data, email=signUp.email.data, name=signUp.name.data, password=generate_password_hash(signUp.password.data, method = 'sha256'), active=1)#use password1 data from form, p2 would work too after our checks
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('routes.homePage'))
    return render_template("/signUp.html", title = 'Create Account', form=signUp)     

@routes.route('/delete-account', methods=['GET', 'POST'])
@login_required
def deleteAccount():
    deleteAccount = AccountDeleteForm()
    if deleteAccount.validate_on_submit():
        username = deleteAccount.username.data
        if username == current_user.username:
            user = User.query.filter_by(username=username).first()
            user.active = 0 #set active column of user table to 0 to indicate inactive user
            db.session.commit()
    return render_template("/deleteAccount.html", form = deleteAccount)
    
@routes.route('/reactivate-account', methods=['GET','POST'])
def reactivateAccount():
    reactivate = ReactivateAccountForm()
    if reactivate.validate_on_submit:
        username = reactivate.username.data
        user = User.query.filter_by(username=username).first()
        user.active = 1
        db.session.commit()
        flash("Account reactivated, continue to login.")
        return redirect(url_for('routes.login'))
    return render_template("/reactivateAccount.html")

@routes.route('add-to-wishlist', methods=['GET', 'POST'])
#@login_required()
def addToWishlist(Title, Link, Price):
    if request.method == 'GET':
        print(Title)
        return render_template("/base.html")
    #if request.method == 'GET':#when route is called from item card or item description
        #request link
        #request item info, to create an item below, we have to have all 'Item' table elements
        #(id, name, price, retailer, )  
        #create item 
        #item = Item(id=id,name=name,price=price,retailer=retailer)
        #get item id: itemID = item.id
        #get user wishlist: wishlist = current_user.wishlist
        #current_user.wishlist = Wishlist(parent_id = user.id, item_id = itemID)
        #db.session.add(current_user.wishlist)
        #db.session.commit()
        #return redirect(url_for("/base.html"))
    #return render_template("/base.html")

#Login page
@routes.route('/login/', methods=["Get", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() #Need to use bcrypt
        #if user.active == 0: #means the user is deactivated
            #flash("Please reactivate account.") 
            #return redirect(url_for('routes.reactivateAccount'))
        if user & user.password == form.password.data:
            login_user(user)
            return redirect(url_for('routes.homePage'))
        else:
            flash('Login unsuccessful, username or password was wrong')
    return render_template("login.html", form=form)

@routes.route('/loggedOut/', methods=["GET"])
def loggedOut():
    return render_template("loggedOut.html")

@routes.route('/product-search/', methods=["GET"])
def productSearchPage():
    form = SearchForm()
    return render_template("productSearch.html", form=form)


@routes.route('/category/<string:category>', methods=["GET"])
def categoryBeauty(category:str):
    return render_template("categorySearch.html", category=category)




@routes.route('/subscription-pricing/', methods=["GET"])
def subscriptionPricingHome():
    return render_template("subscriptionPricing.html")

# Amazon Routes API
#
# Amazon Routes API
#
# Amazon Routes API
@routes.route('/product-search/api/amazon/<string:searchInput>/<string:pageID>/', methods=["POST"])
def productResults(searchInput:str, pageID:int):
    return Amazon(searchInput).getProducts(pageID)

@routes.route('/product-search/api/amazon/bestsellers/', methods=["POST"])
def productSearchHomePageData():
    return Amazon(None).getBestSellerProducts()

@routes.route('/api/get-upc/<string:productASIN>/', methods=["POST"])
def productUPC_API(productASIN:str):
    return Amazon(None).getProductUPC(productASIN)

# Target Routes API
#
# Target Routes API
#
# Target Routes API
@routes.route('/product-search/api/Target/<string:UPC>/<string:amazonProductTitle>/', methods=["POST"])
def targetProductLookUp(UPC:str, amazonProductTitle: str):
    return Target(amazonProductTitle).lookUpProduct_UPC(UPC)

# eBay Routes API
#
# eBay Routes API
#
# eBay Routes API
@routes.route('/product-search/api/eBay/<string:UPC>/', methods=["POST"])
def eBayProductLookUp(UPC:str):
    return eBay(UPC).searchProduct()

# BestBuy Routes API
#
# BestBuy Routes API
#
# BestBuy Routes API
@routes.route('/product-search/api/BestBuy/<string:UPC>/', methods=["POST"])
def bestBuyProductLookUp(UPC:str):
    return BestBuy().searchProductUPC(UPC)

# Rakuten Routes API
#
# Rakuten Routes API
#
# Rakuten Routes API
@routes.route("/api/rakuten/get-cashback/<string:retailer>/", methods=["POST"])
def getRakutenCashback(retailer:str):
    return Rakuten(retailer).rakutenCashBack()
