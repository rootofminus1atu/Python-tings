

def negate(x):
    msg = f"Negating {x}"
    return -x, msg

def square(x):
    msg = f"Squaring {x}"
    return x ** 2, msg


class Logger:
    def __init__(self, value, log=[]):
        self.value = value
        self.log = log
        
    def bind(self, f):
        result, msg = f(self.value)
        return Logger(result, self.log + [msg])
    
test_val = Logger(10).bind(negate).bind(square).bind(negate)
print(test_val.value, test_val.log)

result = (
    Logger(2)
    .bind(negate)
    .bind(square)
    .bind(negate)
    .bind(square)
)
print(result.value, result.log)