from flask import render_template
from DealExpress import flaskObj


@flaskObj.route('/', methods=["GET"])
def homePage():
<<<<<<< Updated upstream
    return render_template("home.html")
=======
    return render_template("home.html")

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

#Login page
@routes.route('/login', methods=["Get", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() #Need to use bcrypt
        if user & user.password == form.password.data:
            login_user(user)
            return redirect(url_for('routes.homePage'))
        else:
            flash('Login unsuccessful, username or password was wrong')
    return render_template("login.html", form=form)

@routes.route('/loggedOut', methods=["GET"])
def loggedOut():
    return render_template("loggedOut.html")

@routes.route('/product-search/', methods=["GET"])
def productSearchPage():
    form = SearchForm()
    return render_template("productSearch.html", form=form)

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
>>>>>>> Stashed changes
