import json
import requests
from fastapi import HTTPException

class apiProvider:

    def __init__(self):
        config_file = f"api/provider/{self.__class__.__name__}.json"
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file) as config:
            return json.load(config)
        
    def get_base_url(self, function):
        api_url = f"{self.config['API_BASE_URL']}/{self.config['API_URLS'][function]}"
        return api_url.replace('{API_KEY}', self.config['API_KEY'])

    def get_response(sef, api_url, no_data_status_code = 404):
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]
            else:
                raise HTTPException(status_code=no_data_status_code, detail="Stock not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error retrieving information")

    def get_stock_price(self, symbol: str):
        raise HTTPException(status_code=501, detail="Not Implemented")
        
    def isin2symbol(self, isin: str):
        raise HTTPException(status_code=501, detail="Not Implemented")
    
    def wkn2symbol(self, wkn: str):
        raise HTTPException(status_code=501, detail="Not Implemented")