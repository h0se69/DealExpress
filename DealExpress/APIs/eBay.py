import json
import tls_client
from bs4 import BeautifulSoup
class eBay():
    def __init__(self, upc: str) -> None:
        self.session = tls_client.Session(client_identifier="chrome_105")
        self.upc = upc
    """
    Fetch eBay products based on UPC given
    """
    def searchProduct(self):
        headers = { 'authority': 'www.ebay.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'max-age=0', 'referer': 'https://www.ebay.com/sch/i.html?_fsrp=1&_from=R40&_nkw=194253397168&_sacat=0&LH_ItemCondition=3&LH_BIN=1&LH_PrefLoc=98&_sop=15', 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"', 'sec-ch-ua-full-version': '"106.0.5249.119"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"macOS"', 'sec-ch-ua-platform-version': '"12.6.0"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', }

        params = {
            '_from': 'R40',
            '_nkw': f'{self.upc}',
            '_sacat': '0',
            'LH_BIN': '1',
            # 'rt': 'nc',
            'LH_ItemCondition': '3',
            '_sop':'15' #Lowest price + shipping param
        }

        self.ebayResponse = self.session.get('https://www.ebay.com/sch/i.html', params=params, headers=headers)
        if(self.ebayResponse.status_code != 200):
            return {
                "ERROR": "STATUS_CODE_INVALID_EBAY"
            }
        else:
            return self.parseEbayResponse()

    """
    Parse eBay request response with BeautifulSoup, call helper functions to
    get Title,Price,Link and return list of products back
    """
    def parseEbayResponse(self):
        bs = BeautifulSoup(self.ebayResponse.text, 'lxml')
        try:
            productCardResponse = bs.find("ul", class_='srp-results srp-list clearfix').find_all('li', class_="s-item s-item__pl-on-bottom s-item--watch-at-corner")
        except AttributeError as attErr:
            return json.dumps({
                    "Title": "N/A",
                    "Price": "NOT_AVAILABLE",
                    "Link": "NOT_AVAILABLE",
                })
        except Exception as e:
            return json.dumps({
                    "Title": "N/A",
                    "Price": "NOT_AVAILABLE",
                    "Link": "NOT_AVAILABLE",
                })
        productList = {}
        for i, product in enumerate(productCardResponse):
            title = self.getTitle(product)
            if(title != None):
                price = self.getPrice(product)
                productLink = self.getProductLink(product)
                productList[i] = {
                    "Title": title,
                    "Price": price,
                    "Link": productLink,
                }
        if(len(productList) >= 1):
            return json.dumps(productList[0], indent=4)
        else:
            return json.dumps(productList, indent=4)


    """
    Get product title
    """
    def getTitle(self, product):
        try:
            return product.find("div", class_="s-item__wrapper clearfix").find("div", class_="s-item__info clearfix").find("div",class_="s-item__title").text
        except:
            return None

    """
    Get product price
    """
    def getPrice(self, product):
        try:
            return product.find("div", class_="s-item__wrapper clearfix").find("div", class_="s-item__info clearfix").find("span",class_="s-item__price").text
        except:
            return None
    """
    Get product link without params
    """
    def getProductLink(self, product):
        try:
            return str(product.find("div", class_="s-item__wrapper clearfix").find("div", class_="s-item__info clearfix").find("a",class_="s-item__link")['href']).split('?')[0]
        except:
            return None

# Request for eBay --> Need to find api endpoint that isnt html reliant
# Need to add async
    # Base works for now

# if __name__ == "__main__":
    # print(eBay("194253397168").searchProduct()) # airpods
    # print(eBay("820650850714").searchProduct()) # pokemon etb lost origins
