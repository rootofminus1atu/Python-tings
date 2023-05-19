from time import time, sleep

def timer(f):
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print(f"Function {f.__name__} took {end - start} seconds")
        return result, end - start
    return wrapper

@timer
def fast(x):
    return x * 2

@timer
def slow(x):
    sleep(2)
    return x * 3

fast(10)
slow(10)





# ugly
def bind(val_and_time, f):
    val, time = val_and_time
    result, time2 = f(val)
    return result, time + time2


class TimedValue:
    def __init__(self, value, time=0):
        self.value = value
        self.time = time
        
    def bind(self, f):
        result, time = f(self.value)
        return TimedValue(result, self.time + time)
    
valtime = TimedValue(10).bind(slow).bind(slow)
print(valtime.value, valtime.time)



class Maybe:
    def __init__(self, value):
        self.value = value
        
    def bind(self, f):
        if self.value is None:
            return self
        
        return f(self.value)

