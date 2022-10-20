import tls_client
from bs4 import BeautifulSoup
class eBay():
    
    def __init__(self, upc: str) -> None:
        self.session = tls_client.Session(client_identifier="chrome_105")
        self.upc = upc

    def searchProduct(self):
        headers = {
            'authority': 'www.ebay.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://www.ebay.com/sch/i.html?_fsrp=1&_from=R40&_nkw=194253397168&_sacat=0&LH_ItemCondition=3&LH_BIN=1&LH_PrefLoc=98&_sop=15',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-full-version': '"106.0.5249.119"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"macOS"',
            'sec-ch-ua-platform-version': '"12.6.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }

        params = {
            '_fsrp': '1',
            'rt': 'nc',
            '_from': 'R40',
            '_nkw': f'{self.upc}',
            '_sacat': '0',
            'LH_BIN': '1',
            '_sop': '15',
            'LH_PrefLoc': '98',
            'LH_ItemCondition': '3',
            '_fss': '1',
            'LH_SellerWithStore': '1',
        }

        self.ebayResponse = self.session.get('https://www.ebay.com/sch/i.html', params=params, headers=headers)
        if(self.ebayResponse.status_code != 200):
            return None
        else:
            self.parseEbayResponse()

    def parseEbayResponse(self):
        bs = BeautifulSoup(self.ebayResponse.text, 'lxml')
        productCardResponse = bs.find("ul", class_='srp-results srp-list clearfix').find_all("li", class_="s-item s-item__pl-on-bottom")
        for product in productCardResponse:
            print(product.find("div", class_="s-item__wrapper clearfix").find("div", class_="s-item__info clearfix").find("div",class_="s-item__title").text) 

# Request for eBay --> Need to find api endpoint that isnt html reliant
if __name__ == "__main__":
    eBay("194253397168").searchProduct()