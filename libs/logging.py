import logging
from pythonjsonlogger import jsonlogger
import logstash
import socket

def setup_logger(logstash_host="logstash", logstash_port=5000, level=logging.INFO):
    logger = logging.getLogger("stock_logger")
    logger.setLevel(level)
    
    # Prevent propagation to the root logger (optional)
    logger.propagate = False

    # Log to file (JSON format)
    file_handler = logging.FileHandler("stock_prices.log")
    file_formatter = jsonlogger.JsonFormatter()
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Log to ELK (via Logstash)
    logstash_handler = logstash.TCPLogstashHandler(logstash_host, logstash_port, version=1, tags=["stock_prices"])
    logstash_formatter = jsonlogger.JsonFormatter()
    logstash_handler.setFormatter(logstash_formatter)
    logger.addHandler(logstash_handler)

    return logger

def log_message(logger, symbol=None, isin=None, price=None, currency=None, exec_time=None, data_provider=None, error=None, info=None, level="info"):

    log_data_all = {
        "Symbol": symbol,
        "ISIN": isin,
        "Price": price,
        "Currency": currency,
        "Exec_Time_sec": exec_time,
        "Data_Provider": data_provider,
        "Error": error,
        "Info": info
    }
    # Filter out None values
    log_data = {key: value for key, value in log_data_all.items() if value is not None}

    if level == "info":
        logger.info(log_data)
    elif level == "error":
        logger.error(log_data)
    elif level == "debug":
        logger.debug(log_data)
    elif level == "warning":
        logger.warning(log_data)
    else:
        logger.info(log_data)