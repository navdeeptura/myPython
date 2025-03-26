import time
from functools import wraps

def measure_latency(func):
    """Decorator to measure the function latency in ms"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        latency = (end_time - start_time) * 1000 # convert to miliseconds
        print(f"Function '{func.__name__}' Latency: '{latency:.4f}' ms")

        return result

    return wrapper

@measure_latency
def test_one_second():
    time.sleep(1)
    print("Sleep Time")

#test_one_second()

def italics(func):
    """add italics in the word"""

    def wrapper():
        return f"<i>'{func()}' </i>"
    return wrapper

@italics
def test_italic_bold():
    return "This is sample string"



def bold(func):
    def wrapper():
        return f"<strong> '{func()}' </strong>"
    return wrapper()

if __name__ == '__main__()':
    print(test_italic_bold())

