from flask import render_template, Blueprint

from DealExpress.APIs.amazon import Amazon
from DealExpress.APIs.target import Target
#from DealExpress import flaskObj

routes = Blueprint('routes', __name__)

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