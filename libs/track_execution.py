import time, functools
from .logging import log_message

def track_execution_time_old(logger):
    print("Tracker")
    def decorator(func):
        print(f"xxx {func}")
        async def wrapper(*args, **kwargs):
            print("Wrapper")
            start_time = time.time()
            print(start_time)
            
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
            isin_result = result.get('isin') if result and isinstance(result, dict) else None
            if isin_result is not None:
                isin = isin_result
            symbol_result = result.get('symbol') if result and isinstance(result, dict) else None
            if symbol_result is not None:
                symbol = symbol_result

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


def time_it(func):
    import time
    @functools.wraps(func)
    async def wrapper(*args,**kwargs):
        start = time.time()
        print(f"Before await {func}")
        result = await func(*args,**kwargs)
        print(f"After await {func}")
        end_time = time.time()
        execution_time = end_time - start
        print(f"Execution time: {execution_time:.3f} seconds")
        #logger(f'time taken by {func.__name__} is {time.time()-start }')
        return result
    return wrapper

