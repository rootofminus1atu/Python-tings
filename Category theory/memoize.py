

def memoizator(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper

@memoizator
def fibo(n):
    if n < 2:
        return n
    return fibo(n-1) + fibo(n-2)

for i in range(100):
    print(fibo(i))
    
    
cache2 = {}

def fibo2(*args):
    if args not in cache2:
        cache2[args] = fibo(*args)
    return cache2[args]

for i in range(100):
    print(fibo2(i))
    
    

@memoizator
def funny_fibo(n, str):
    if n < 2:
        return n
    return funny_fibo(n-1, str) + funny_fibo(n-2, str)

for i in range(100):
    print(funny_fibo(i, "hello"))

    
    


def ackermann(m, n):
    print(f"({m}, {n})")
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))

print(ackermann(3,4))