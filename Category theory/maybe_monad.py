import math

class Maybe:
    def __init__(self, value):
        self.value = value
        
    def bind(self, f):
        if self.value is None:
            return Maybe(None)  # equivalent to `self`, pretty funny
        
        return Maybe(f(self.value))
    
    def __repr__(self):
        return f"Maybe({self.value})"
    
def sqrt(x):
    if x < 0:
        return None
    
    return math.sqrt(x)

def reciprocal(x):
    if x == 0:
        return None
    
    return 1 / x

def add1(x):
    return x + 1

def root_reciprocal(x):
    return Maybe(x).bind(sqrt).bind(reciprocal).value

num = Maybe(-1).bind(add1).bind(reciprocal).bind(add1)
print(num)


class MaybeBetter:
    def __init__(self, value):
        self.value = value
        
    def bind(self, f):
        if self.value is None:
            return self
        
        return f(self.value)
    
    def __repr__(self):
        return f"MaybeBetter({self.value})"
    
    def sqrt(self):
        return self.bind(sqrt)
    
    def reciprocal(self):
        return self.bind(reciprocal)
    
    def log(self):
        if self.value <= 0:
            return Maybe(None)
        
        return Maybe(math.log(self.value))
    
num2 = MaybeBetter(-1).log()

print(num2)