from typing import Iterable
from time import time, sleep


def timer(f):
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print(f"Function {f.__name__} took {end - start} seconds")
        return result
    return wrapper

class ListBetter:
    def __init__(self, value: Iterable):
        self.value = value
        self.original_type = type(value)
        
    def __repr__(self):
        return f"{self.value}"
    
    def __getitem__(self, index):
        return self.value[index]
    
    def __setitem__(self, index, value):
        self.value[index] = value
    
    def _create_instance(self, val):
        return ListBetter(self.original_type(val))
    
    def map(self, func):
        return self._create_instance(map(func, self.value))
    
    def filter(self, func):
        return self._create_instance(filter(func, self.value))
    
"""
import timeit

lst = [x for x in range(10000)]

def test_map_listbetter():
    better = ListBetter(lst)
    new = better.map(lambda x: x + 1)

def test_map_builtin():
    newer = list(map(lambda x: x + 1, lst))



lst = [x for x in range(10000)]
    
for i in [100, 500, 1000, 10000]:
    time_listbetter = timeit.timeit(test_map_listbetter, number=i)
    time_builtin = timeit.timeit(test_map_builtin, number=i)
    print(f"Time taken by ListBetter with {i} tries:", time_listbetter)
    print(f"Time taken by built-in map with {i} tries:", time_builtin)
    print()

"""


class IterBetter:
    def __init__(self, value: Iterable, log=[]):
        self.value = value
        self.log = log
        self.original_type = type(value)
        
    def __repr__(self):
        return f"{self.value}"
    
    def __getitem__(self, index):
        return self.value[index]
    
    def __setitem__(self, index, value):
        self.value[index] = value
        
    @staticmethod
    def with_bind(f):
        
        def wrapper(self, func):
            result, msg = f(self, func)
            return self._create_instance(self.original_type(result), self.log + [msg])
        
        return wrapper
    
    def _create_instance(self, val):
        return IterBetter(self.original_type(val), self.log)
    
    @with_bind
    def map(self, func):
        msg = f"Mapping {func} over {self.value}"
        return self._create_instance(map(func, self.value)), msg
    
    @with_bind
    def filter(self, func):
        msg = f"Filtering {func} over {self.value}"
        return self._create_instance(filter(func, self.value)), msg
    
    
mylst = IterBetter([1,2,3,4,5])
newlst = (
    mylst
    .map(lambda x: x + 1)
    .map(lambda x: x + 1)
    .map(lambda x: x + 1)
)

print(newlst.log)
print(newlst)