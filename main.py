from fastapi import FastAPI, HTTPException
from libs.logging import setup_logger
from libs.track_execution import track_execution_time
from api.api_libs.net_lib import get_ip_address

# Setup logger
logger = setup_logger()

# Create FastAPI app
app = FastAPI()

# Decorate the root path with execution time tracking
@track_execution_time(logger)
@app.get("/", response_model=dict)
async def read_root():
    return {"info": "Welcome to the Finance API"}

@track_execution_time(logger)
@app.get("/status", response_model=dict)
async def get_status():
    ip_address = get_ip_address()
    return {"ip": ip_address, "status": "running"}

@track_execution_time(logger)
@app.get("/stock_price_isin", response_model=dict)
async def get_stock_price_isin(isin: str):
    print(isin)
    return {'price': 0.0, 'currency': 'xxx'}
