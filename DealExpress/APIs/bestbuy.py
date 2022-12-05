import json
import random
import uuid
import tls_client
import difflib

class BestBuy():
    
    def __init__(self) -> None:
        self.session = tls_client.Session(client_identifier="chrome_105")

    def searchProductUPC(self, UPC):
        headers = {
            'authority': 'www.bestbuy.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.bestbuy.com',
            'referer': 'https://www.bestbuy.com/site/searchpage.jsp?st=194252165959&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }

        json_data = {
            'blueprint': '',
            'component': 'NINJA',
            'componentId': 'shop-ninja-26631621',
            'componentVersion': 'not provided',
            'deviceAndBrowser': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'event': 'CLOAD',
            'mversion': 1,
            'pageType': 'SLP',
            'platform': 'L',
            # 'sessionId': self.genUUID(),
            # 'visitorId': self.genUUID(),
            # 'breadcrumb': '/6011/BestBuyDesktopWeb/search_results/computers_x_tablets/laptops/194252165959',
            'keywords': f'{UPC}',
            # 'pageTransactionId': self.genUUID(),
            # 'pageSkuId': '6418601',
        }

        bbResponse = self.session.post('https://www.bestbuy.com/awacs-ingestor/api/cload', headers=headers, json=json_data)
        bbJsonResponse = bbResponse.json()
        print(bbJsonResponse)
        return json.dumps({
            "Link": self.getSKU(bbJsonResponse),
            "Price": self.getSKU(bbJsonResponse)
        }, indent=4)

    def getSKU(self, product):
        try:
            return f'https://www.bestbuy.com/site/h0seFNF/{product["pageSkuId"]}.p?skuId={product["pageSkuId"]}'
        except ValueError as valError:
            return f"NO_SKU_FOUND_{valError}"

    def getPrice(self, product):
        try:
            return product["currentPrice"]
        except ValueError as valError:
            return f"NO_PRICE_FOUND_{valError}"

    """Generate random UUID Usually for headers/url"""
    def genUUID(self):
        return str(uuid.uuid4())

# print(BestBuy().searchProductUPC("194252165959"))