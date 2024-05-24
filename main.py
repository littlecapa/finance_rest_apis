from fastapi import FastAPI, HTTPException
import requests

API_KEY = "cHls4n1Au95DZ5VMkk3twH3y2SUyZxg1"

app = FastAPI()

@app.get("/stock_price/{symbol}")
async def get_stock_price(symbol: str):
    # Replace with the actual API endpoint and key
    api_url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
        else:
            raise HTTPException(status_code=404, detail="Stock not found")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error retrieving stock information")
