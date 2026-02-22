import time
import functools

def retry_on_failure(max_retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"Retrying {func.__name__} after exception: {e} (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                    else:
                        print(f"{func.__name__} failed after {max_retries} retries.")
                        raise
        return wrapper
    return decorator
