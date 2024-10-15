import logging
from pythonjsonlogger import jsonlogger
import logstash
import socket
import time
import json

class Stack:
    def __init__(self):
        self.items = []

    def push(self, element):
        self.items.append(element)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

        else:
            raise IndexError("Stack is empty")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Stack is empty")

    def is_empty(self):
        return len(self.items) == 0
    
    def __str__(self):
        # String representation of the stack
        return f"Stack: {str(self.items)}"
    
class StackElement:
    def __init__(self, start_time, function_name):
        self.start_time = start_time
        self.function_name = function_name

    def __str__(self):
        # String representation of the stack
        return f"{self.start_time} {self.function_name}\n"

class BytesFormatter(jsonlogger.JsonFormatter):
        def format(self, record):
            message = super().format(record)
            return message.encode('utf-8')  # Encode the message as bytes

class Log_Singelton:
    _instance = None

    def __new__(cls, logger_name="stock_api_logger", logstash_host="logstash", logstash_port=5000, level=logging.INFO):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.logger = cls.setup_logger(logger_name=logger_name, logstash_host=logstash_host, logstash_port=logstash_port, level=level)
            cls.stack = Stack()
        return cls._instance
    
    def setup_logger(logger_name, logstash_host, logstash_port, level):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # Prevent propagation to the root logger (optional)
        logger.propagate = False

        # Log to file with a custom format
        file_handler = logging.FileHandler(logger_name + ".log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Log to ELK (via Logstash)
        logstash_handler = logstash.TCPLogstashHandler(logstash_host, logstash_port, version=1, tags=[logger_name])
        logstash_formatter = BytesFormatter()
        logstash_handler.setFormatter(logstash_formatter)
        logger.addHandler(logstash_handler)

        return logger
    
    def start_execution(cls, function_name):
        cls.stack.push(StackElement(start_time=time.time(), function_name=function_name))

    def log_execution(cls, function_name, status, symbol=None, isin=None, price=None, currency=None, info=None, level="info"):
        top = cls.stack.pop()
        if top.function_name != function_name:
            raise Exception(f"Stack out of Sync {top.function_name} {function_name}")
        exec_time = (time.time()-top.start_time)
        log_data_all = {
            "Function": function_name,
            "Status": status,
            "Symbol": symbol,
            "ISIN": isin,
            "Price": price,
            "Currency": currency,
            "Exec_Time_sec": exec_time,
            "Info": info
        }
        cls.log_log_data(log_data_all, level)
    
    def log_log_data(cls, log_data_all, level):
        log_data = json.dumps({key: value for key, value in log_data_all.items() if value is not None})
        if level == "info":
            cls.logger.info(log_data)
        elif level == "error":
            cls.logger.error(log_data)
        elif level == "debug":
            cls.logger.debug(log_data)
        elif level == "warning":
            cls.logger.warning(log_data)
        else:
            cls.logger.info(log_data)
        
    def log_info_message(cls, message):
        cls.logger.info(message)

    def log_error(cls, status, error_message, exit_function = False):
        if exit_function:
            top = cls.stack.pop()
        else:
            top = cls.stack.peek()
        log_data = {
            "Function": top.function_name ,
            "Status": status,
            "Error": error_message
        }
        cls.log_log_data(log_data, "error")

 