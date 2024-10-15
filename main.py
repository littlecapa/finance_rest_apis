from fastapi import FastAPI, HTTPException
from libs.log_singleton import Log_Singelton
from api.api_libs.net_lib import get_ip_address
from api.api_manager import apiManager
import logging

# Setup logger
mylog = Log_Singelton(logger_name="stock_api_logger", logstash_host="logstash", logstash_port=5000, level=logging.INFO)
mylog.log_info_message("App started")

# Create FastAPI app
app = FastAPI()
api_manager = apiManager(mylog)


@app.get("/", response_model=dict)
async def read_root():
    return get_health()

@app.get("/health", response_model=dict)
def get_health():
    mylog.start_execution("/health")
    ip_address = get_ip_address()
    mylog.log_execution("/health", status = 200)
    return {"ip": ip_address, "status": 200}

@app.get("/stock_price_isin", response_model=dict)
async def get_stock_price_isin(isin: str):
    mylog.start_execution("/stock_price_isin")
    price = None
    currency = None
    status = 200
    try:
        if not isin:
            status = 400
            mylog.log_error(status, "No ISIN in Request")
        price, currency = api_manager.get_price_isin(isin)
    except HTTPException as e:
        mylog.log_error(e.status_code, e.detail)
        raise HTTPException(e.status_code, e.detail)

    mylog.log_execution("/stock_price_isin", status = status, isin=isin)
    return {'price': price, 'currency': currency, 'status': status}
