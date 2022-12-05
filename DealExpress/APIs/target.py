import json
import random
import string
import tls_client
import difflib

class Target():
    """
    Init class + TLS Client Session
    @param amazonProductTitle = amazonProductTitle from Amazon Class 
    """
    def __init__(self, amazonProductTitle) -> None:
        self.session = tls_client.Session(client_identifier="chrome_105")
        self.amazonProductTitle = amazonProductTitle

    """
    Looks up the amazonProduct on target using the UPC 
    Returns the products title, price, sku in json format
    """
    def lookUpProduct_UPC(self, upc):
        headers = { 'authority': 'redsky.target.com', 'accept': 'application/json', 'accept-language': 'en-US,en;q=0.9', 'origin': 'https://www.target.com', 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', }

        params = {
            'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96', #API KEY
            'channel': 'WEB',
            'count': '28',
            'default_purchasability_filter': 'true',
            'include_sponsored': 'false',
            'keyword': f'{upc}',
            'offset': '0',
            'page': f'/s/{upc}',
            'platform': 'desktop',
            'pricing_store_id': '1927',
            'visitor_id': self.random32String(), # Random 32 Gen/ Might need to add USERAGENT param
        }

        targetResponse = self.session.get('https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2', params=params, headers=headers)
        try:
            jsonProductsData = targetResponse.json()["data"]["search"]["products"]
        except KeyError as keyError:
            return {"ERROR": "INVALID_JSON_RESPONSE"}
        except Exception as exception:
            return {"ERROR": exception}
            
        highestMatchingRate = 0
        closestMatchingProductDic = {}
        for product in jsonProductsData:
            try:
                price = self.getPrice(product)
                title = self.getTitle(product)
                tcin = self.getTCIN(product)
                productEqualityRatio = self.checkProductEqualityRatio(title)

                if(productEqualityRatio >= highestMatchingRate):
                    closestMatchingProductDic = {
                        "Title": title, 
                        "Price": price, 
                        "Link": f"https://www.target.com/p/h0seFNF/A-{tcin}"
                    }
                    highestMatchingRate = productEqualityRatio
            except Exception as e:
                continue
        return json.dumps(closestMatchingProductDic, indent=4)

    """
    Generates a random 32 length string for random visitorId headers
    """
    def random32String(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits +string.ascii_lowercase, k=32))

    """
    Get target product title
    """
    def getTitle(self, product):
        try:
            return product["item"]["product_description"]["title"]
        except ValueError as valError:
            return f"NO_TITLE_FOUND_{valError}"
    """
    Get target product price
    """
    def getPrice(self, product):
        try:
            return product["price"]["formatted_current_price"]
        except ValueError as valError:
            return f"NO_PRICE_LISTED_{valError}"

    """
    Get target product TCIN/SKU
    """
    def getTCIN(self, product):
        try:
            return product["tcin"]
        except ValueError as valError:
            return f"NO_TCIN_{valError}"

    """
    Compare amazonProductTitle and Target product title for similarity 
    with UPC as the search KW
    """
    def checkProductEqualityRatio(self, title):
        try:
            return difflib.SequenceMatcher(None, self.amazonProductTitle, title).ratio() * 100
        except:
            return 0        


# print(Target("Pokemon TCG: SAS11 —Lost Origin Elite Trainer Box").lookUpProduct_UPC("820650850714"))
