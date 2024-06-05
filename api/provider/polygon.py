import json
import requests
from fastapi import HTTPException
from api.provider.api_provider import apiProvider

class polygon(apiProvider):

    def get_stock_price(self, symbol: str):
        api_url = self.get_base_url('quote')
        api_url = api_url.replace('{symbol}', symbol)
        return self.get_response(api_url, 404)