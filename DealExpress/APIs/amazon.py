import json
import tls_client
from bs4 import BeautifulSoup
import re

class Amazon():
    """
    Init class + TLS Client Session
    @param searchInput = userInput 
    """
    def __init__(self, searchInput:str) -> None:
        self.session = tls_client.Session(client_identifier="chrome_105")
        self.searchInput = searchInput

    """
    Fetch Amazons best sellers page for electronics
    + Parses the HTML with Beautifulsoup
    Future change: Use JSON endpoint for faster response time
    Will change it to rotate between all the categories they have
    """
    def getBestSellerProducts(self):
        headers = { 'authority': 'www.amazon.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'no-cache', 'device-memory': '8', 'downlink': '10', 'dpr': '1', 'ect': '4g', 'pragma': 'no-cache', 'referer': 'https://www.amazon.com/gp/new-releases/ref=zg_bs_tab', 'rtt': '100', 'sec-ch-device-memory': '8', 'sec-ch-dpr': '1', 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-viewport-width': '2560', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 'viewport-width': '2560', }

        bestSellersResponse = self.session.get('https://www.amazon.com/gp/new-releases/electronics/ref=zg_bsnr_nav_0', headers=headers)
        bs = BeautifulSoup(bestSellersResponse.text, 'lxml')
        productList = bs.find_all("div", class_="p13n-sc-uncoverable-faceout")

        productDic = {}
        if(not productList):
            return None
        else:
            for i, product in enumerate(productList):
                asin = self.getASIN(product)
                if(asin != "INVALID_ASIN"):
                    title = self.getTitle(product)
                    price = self.getPrice(product)
                    imageUrl = self.getImage(product)
                    productDic[i] = asin, title, price, imageUrl
                else:
                    continue
        return json.dumps(productDic, indent=4)

    """
    Return Amazon ASIN
    """
    def getASIN(self, product):
        try:
            return product["id"]
        except ValueError as valError:
            return "INVALID_ASIN"

    """
    Return Amazon Image Src_url
    """
    def getImage(self, product):
        try:
            return product.findChild("img")['src']
        except ValueError as valError:
            return "https://uploads-us-west-2.insided.com/looker-en/attachment/d0a25f59-c9b7-40bd-b98e-de785bbd04e7.png"
        
    """
    Return Amazon product price
    """
    def getPrice(self, product):
        try:
            return product.find("span", class_="a-size-base a-color-price").find('span').text
        except AttributeError as backupFindPrice:
            try:
                return product.find("span", class_="a-price").find('span', class_='a-offscreen').text
            except ValueError as valError:
                return "NFS_VALERR"
            except Exception as erro:
                return "NFS_ERR"
        except ValueError as valError:
            return "NFS_VALERR"
        except Exception as erro:
            return "NFS_ERR"
    """
    Return Amazon Product title
    """
    def getTitle(self, product):
        try:
            return product.find("span", class_=re.compile("a-size-medium a-color-base a-text-normal|a-size-base a-color-base a-text-normal|a-size-base-plus a-color-base a-text-normal")).text
        except AttributeError as backupFindTitle:
            try:
                return product.find("span").text
            except ValueError as valError:
                return "NO_TITLE_VALERR"
            except Exception as erro:
                return "NO_TITLE_ERR"                
        except ValueError as valError:
            return "NO_TITLE_VALERR"
        except Exception as erro:
            return "NO_TITLE_ERR"
      
        
    """
    Uses Amazons suggessted search API to help autocomplete our search bar input
    (Limited to 5)
    """
    def getSuggestedSearchResults(self):
        headers = { 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive', 'Origin': 'https://www.amazon.com', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', }

        params = {
            'limit': '10',
            'prefix': self.searchInput,
            'suggestion-type': [
                'WIDGET',
                'KEYWORD',
            ],
            'page-type': 'Gateway',
            'alias': 'aps',
            'site-variant': 'desktop',
            'version': '3',
            'event': 'onkeypress',
            'wc': '',
            'lop': 'en_US',
            'avg-ks-time': '307',
            'fb': '1',
            'mid': 'ATVPDKIKX0DER',
            'plain-mid': '1',
            'client-info': 'amazon-search-ui',
        }

        amazonCompletionResponse = self.session.get('https://completion.amazon.com/api/2017/suggestions', params=params, headers=headers)
        for i, suggestionResult in enumerate(amazonCompletionResponse.json()["suggestions"]):
            if(i<5):
                print(suggestionResult["value"]) # Wont be implemented as of now
            else:
                break

    """
    Get Products based on the SearchInput, while incrementing the pageNumber(PageID)
    when the user reaches the bottom of the html page
    """
    def getProducts(self, pageID):
        headers = { 'authority': 'www.amazon.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'en-US,en;q=0.9', 'device-memory': '8', 'downlink': '10', 'dpr': '1', 'ect': '4g', 'referer': 'https://www.amazon.com/', 'rtt': '0', 'sec-ch-device-memory': '8', 'sec-ch-dpr': '1', 'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-viewport-width': '2560', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 'viewport-width': '2560', }
        params = { 'k': self.searchInput, 'page': pageID }

        productResponse = self.session.get('https://www.amazon.com/s', params=params,  headers=headers)
        bs = BeautifulSoup(productResponse.text, 'lxml')
        productList = bs.find_all("div", attrs={"data-index":re.compile("^[0-9]")})

        productDic = {}
        if(not productList):
            return None
        else:
            for i, product in enumerate(productList):
                try:
                    productASIN = product.find("div", attrs={"data-csa-c-item-id": True})
                    if("amzn1.asin.1." in productASIN["data-csa-c-item-id"]):
                        asin = productASIN["data-csa-c-item-id"].replace("amzn1.asin.1.","")
                        title = self.getTitle(product)
                        price = self.getPrice(product)
                        imageUrl = self.getImage(product)
                        productDic[i] = asin, title, price, imageUrl
                    else:
                        continue
                except Exception as e:
                    continue

        return json.dumps(productDic, indent=4)


    def getProductUPC(self, productASIN):
        headers = { "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-language": "en-US,en;q=0.9", "cache-control": "max-age=0", "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "document", "sec-fetch-mode": "navigate", "sec-fetch-site": "none", "sec-fetch-user": "?1", "upgrade-insecure-requests": "1" }

        apiResponse = self.session.post(f"https://paid-h0sefnf-amazonapi.herokuapp.com/api/get-upc/?productASIN={productASIN}", headers=headers)
        if(apiResponse.status_code != 200):
            return {
                "ERROR": "INVALID_RESPONSE_CODE_API_UPC"
            }
        else:
            try:
                return apiResponse.json()
            except:
                return {
                    "ERROR": "INVALID_JSON_RESPONSE_API_UPC"
                }
