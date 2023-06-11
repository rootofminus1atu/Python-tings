# no loops no ifs no lists no side-effects no 2-argument functions


def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

for i in range(6):
    print(f"{i}! = {factorial(i)}")





def sum(a, b):
    return a + b

def sum_pure(a):
    def sum_pure2(b):
        return a + b
    return sum_pure2

sum_pure_pure = lambda a: lambda b: a + b
sum_not_pure = lambda a, b: a + b

print(f"2 + 3 = {sum_pure(2)(3)}")
print(f"2 + 3 = {sum_pure_pure(2)(3)}")
print(f"2 + 3 = {sum_not_pure(2, 3)}")





class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    @staticmethod
    def create(a):
        return lambda b: Pair(a, b)
    
    def head(self):
        return self.first
    
    def tail(self):
        return self.second
    
    def __repr__(self) -> str:
        return f"({self.first}, {self.second})"
    

    def to_list(self):
        copy = self
        result = []

        while (copy != None):
            result.append(copy.head())
            copy = copy.tail()

        return result
    
    @staticmethod
    def list_to_pairing(lst):
        lst.reverse()
        result = None

        for n in lst:
            result = Pair.create(n)(result)

        return result


p1 = Pair.create(5)(2)
print(f"p1 = ({p1.head()}, {p1.tail()})")

lest = Pair.create(7) (Pair.create(6) (Pair.create(5) (None)))

print(f"list thing: [{lest.head()}, {lest.tail().head()}, {lest.tail().tail().head()}]")
print(lest)
print(lest.to_list())
print(Pair.list_to_pairing([1, 2, 3, 4]))




ranger = lambda low: lambda high: None if low > high else Pair.create(low) (ranger(low + 1) (high))

print(ranger(1)(10))


mapper = lambda func: lambda pairing: \
    None if pairing is None \
    else Pair.create(func(pairing.head())) (mapper(func)(pairing.tail())) 

print(mapper(lambda x: x**2)(ranger(1)(10)))


fizzbuzz = lambda n: ("Fizz" if n % 3 == 0 else "") + ("Buzz" if n % 5 == 0 else "") or n

print(mapper(fizzbuzz)(ranger(1)(30)))
