import time
from .logging import log_message


def track_execution_time(logger):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # Call the actual function
            result = await func(*args, **kwargs)
            
            # Calculate execution time
            execution_time = (time.time() - start_time)*1e3
            
            # Extract parameters (assuming ISIN or Symbol in args/kwargs)
            isin = kwargs.get('isin') if 'isin' in kwargs else None
            symbol = kwargs.get('symbol') if 'symbol' in kwargs else None
            
            # Extract data from result (assuming result is a dict or similar structure)
            price = result.get('price') if result and isinstance(result, dict) else None
            currency = result.get('currency') if result and isinstance(result, dict) else None
            info = result.get('info') if result and isinstance(result, dict) else None
            log_message(
                logger,
                symbol=symbol,
                isin=isin,
                price=price,
                currency=currency,
                exec_time=execution_time,
                data_provider=func.__name__, 
                error=None, 
                info=info, 
                level="info"
            )
            return result

        return wrapper
    return decorator