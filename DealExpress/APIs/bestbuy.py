import json
import random
import tls_client
import difflib

class BestBuy():
    
    def __init__(self) -> None:
        self.session = tls_client.Session(client_identifier="chrome_105")

    def searchProductUPC(self, UPC):
        pass

    def searchProductKeyword(self, keyword):
        pass
