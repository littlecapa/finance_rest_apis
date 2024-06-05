import json
import requests
from fastapi import HTTPException
from api.provider.api_provider import apiProvider

class financeModeling(apiProvider):

    def get_stock_price(self, symbol: str):
        api_url = self.get_base_url('quote')
        api_url = api_url.replace('{symbol}', symbol)
        return self.get_response(api_url, 404)
        
    def isin2symbol(self, isin: str):
        api_url = self.get_base_url('lookup_isin')
        api_url = api_url.replace('{isin}', isin)
        return self.get_response(api_url, 404)
    
    def wkn2symbol(self, wkn: str):
        print("Start API")
        api_url = self.get_base_url('lookup_wkn')
        api_url = api_url.replace('{wkn}', wkn)
        print(api_url)
        return self.get_response(api_url, 404)