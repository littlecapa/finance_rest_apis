from fastapi import FastAPI, HTTPException
from libs.log_singleton import Log_Singelton
from api.api_libs.net_lib import get_ip_address
import logging

# Setup logger
mylog = Log_Singelton(logger_name="stock_api_logger", logstash_host="logstash", logstash_port=5000, level=logging.INFO)
mylog.log_info_message("App started")

# Create FastAPI app
app = FastAPI()

#@track_execution_time(logger)
#@app.get("/", response_model=dict)
#async def read_root():
#    print("Root")
#    return {"info": "Welcome to the Finance API"}

#@track_execution_time(logger)

@app.get("/health", response_model=dict)
def get_health():
    mylog.start_execution(__name__)
    ip_address = get_ip_address()
    mylog.log_execution(__name__, info="Status Ok")
    return {"ip": ip_address, "status": "ok"}

#@track_execution_time(logger)
#@app.get("/stock_price_isin", response_model=dict)
#async def get_stock_price_isin(isin: str):
#    if not isin:
#        raise HTTPException(status_code=400, detail="Invalid ISIN")
#    return {'price': 0.0, 'currency': 'xxx'}
