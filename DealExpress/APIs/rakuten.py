import base64
from datetime import datetime
import json
import tls_client
import uuid
import re

class Rakuten():
    
    def __init__(self, retailer: str) -> None:
        self.session = tls_client.Session(client_identifier="chrome_105")
        self.retailer = retailer

    """
    Get Rakuten Cashback based on retailer (Priority Method)
    """
    def rakutenCashBack(self):
        headers = { 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive', 'Referer': 'https://www.rakuten.com/', 'Sec-Fetch-Dest': 'script', 'Sec-Fetch-Mode': 'no-cors', 'Sec-Fetch-Site': 'same-site', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', }
        jsonpValue = f"jsonp_{self.genUUID()}"
        # Request error = falls back to brute froce method
        try:
            rakutenResponse = self.session.get(f'https://rewards.api.search-suggest.rakuten.com/search/v2/us_rewards_search/store.json?query=cf_text:%22{self.retailer}%22&sid=us_rewards_ac_001&json.wrf={jsonpValue}', headers=headers)
        except:
            self.rakutenCashBack_BruteForce()

        rakutenResponseParsed = re.sub(jsonpValue, "", rakutenResponse.text)
        rakutenResponseJSON = json.loads(re.sub(r"[()\n]", "", rakutenResponseParsed))
        if(self.retailer in json.dumps(rakutenResponseJSON)):
            try:
                for retailer in rakutenResponseJSON['response']['docs']:
                    if(re.search(self.retailer, retailer['u'], flags=re.IGNORECASE)):
                        return {
                            "CashbackAmount": retailer['c']
                        }
                return {
                    "ERROR": f"NO_CASHBACK_FOUND_FOR_{self.retailer.upper()}"
                }            
            except Exception as error:
                print(str(error).upper().replace(" ", "_"))
                pass
        else:
            return {
                "ERROR": f"{self.retailer.upper()}_NOT_AVAILABLE_FOR_CASHBACK_REWARDS"
            }

    """
    Fallback method for getting Rakuten Cashback 
    if rakuten_StoreSearch() were to timeout/fail
    """
    def rakutenCashBack_BruteForce(self):
        headers = { 'authority': 'www.rakuten.com', 'accept': 'application/json, text/plain, */*', 'accept-language': 'en-US,en;q=0.9', 'client-agent': 'rr-bih-feweb', 'referer': 'https://www.rakuten.com/stores/all', 'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 'x-anonymous-id': self.genUUID(), 'x-platform': 'DESKTOP_WEB', }
        cursorString = ""
        start = 0
        
        params = {
            'topicId': '16867',
            'entityIds': '',
            'sort': '',
            'filter': 'category:',
            'cursor': cursorString,
        }
        while(True):
            rakutenResponse = self.session.get('https://www.rakuten.com/feedapi/v1/topic', params=params, headers=headers)
            try:
                cashBackJSON = rakutenResponse.json()['data']['viewer']['topic']['items']['edges']
                if(self.retailer in json.dumps(cashBackJSON)):
                    for retailer in cashBackJSON:
                        try:
                            retailerName = retailer['node']['itemData']['merchantname_text']
                            retaierCashbackAmount = retailer['node']['itemData']['currentreward_rewardtext']
                            if(re.search(self.retailer, retailerName, flags=re.IGNORECASE)):
                                return {
                                    "CashbackAmount": retaierCashbackAmount
                                }
                        except:
                            pass
                    return {
                        "ERROR": f"NO_CASHBACK_FOUND_FOR_{self.retailer.upper()}"
                    }                     
                elif(cashBackJSON == []):
                    return {
                        "ERROR": "BRUTE_FORCE_LIMIT_REACHED_AKA_STORE_DOES_NOT_OFFER_CASHBACK"
                    }    
                else:
                    start += 120
                    end = start - 1
                    cursorBase64 = base64.b64encode(f"topic16867-{start}-{end}".encode('ascii'))
                    cursorString = cursorBase64.decode('utf-8')
                    params['cursor'] = cursorString
            except Exception as exceptionError:
                print(str(exceptionError).upper().replace(" ", "_"))
                return None

    """Generate random UUID Usually for headers/url"""
    def genUUID(self):
        return str(uuid.uuid4())

# if __name__ == "__main__":
#     print(f"bruteforce-start: {datetime.now().time()}")
#     Rakuten("ebay").rakuten_BruteForceSearch()
#     print(f"bruteforce-end: {datetime.now().time()}\n")

#     print(f"normal-start: {datetime.now().time()}")
#     Rakuten("ebay").rakuten_StoreSearch()
#     print(f"normal-end: {datetime.now().time()}")
