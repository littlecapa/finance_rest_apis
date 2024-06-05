import json
import requests
from fastapi import HTTPException
from api.provider.api_provider import apiProvider

class openFigi(apiProvider):

    def __init__(self):
        super().__init__()
        self.headers = {
            'Content-Type': 'application/json',
            'X-OPENFIGI-APIKEY': self.config['API_KEY']
        }
        
    def get_response(self, idType, idValue, api):
        body = [{
            "idType": idType,
            "idValue": idValue
        }]
        response = requests.post(f"{self.config['API_BASE_URL']}{self.config['API_URLS'][api]}", headers=self.headers, json=body)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]
            else:
                raise HTTPException(status_code=404, detail="ISIN not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error retrieving data")
    
    def isin2symbol(self, isin: str):
        return self.get_response(idType = "ID_ISIN", idValue = isin, api = 'lookup_isin')
    
    def wkn2symbol(self, wkn: str):
        return self.get_response(idType = "ID_WKN", idValue = wkn, api = 'lookup_wkn')