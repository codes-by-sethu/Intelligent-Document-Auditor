import time
from functools import wraps

def trace_performance(func):
    """Decorator to measure execution time of auditor functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        # In a real scenario, you'd log this to a file or DB
        print(f"DEBUG: {func.__name__} took {duration:.2f} seconds.")
        return result, duration
    return wrapper