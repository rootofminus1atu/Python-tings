import math

class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
jeff = Human("Jeff", 21)
jeff = "new name"

# TODO:
# RESEARCH DESCRIPTORS 


# stack + heap = sheep
sheep = {}

class Cell:
    def __init__(self, value, address):
        self.value = value
        self.address = address
        sheep[address] = self
        
    def __repr__(self):
        return f"Cell({self.value}, {self.address})"
        
    
class Address:
    def __init__(self, address):
        self.address = address
        
    
    def __repr__(self):
        return f"Address({self.address})"
    
    def dr(self):
        return sheep[self.address]
        

n = Cell(6, 100)
print(n)

ptr = Address(n.address)
print(ptr)

m = ptr.dr()
print(m)

# ptr.dr() = 7

        
        