# utils/profiler.py
# Placeholder for optional latency and performance measurement tools.

import time
from functools import wraps

def measure_latency(func):
    """A decorator to measure the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[Profiler] {func.__name__} took {end_time - start_time:.4f} seconds.")
        return result
    return wrapper