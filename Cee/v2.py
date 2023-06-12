sheep = {}

class Cell:
    def __init__(self, value, address):
        self.value = value
        self.address = address
        sheep[address] = self

    def __repr__(self):
        return f"Cell({self.value}, {self.address})"
    
    def dr_and_set(self, value):
        target = sheep[self.value]
        target.value = value
        
    
    
n = Cell(6, 100)
print(n)  # Output: Cell(6, 100)

ptr = Cell(n.address, 108)
print(ptr)  # Output: Cell(100, 108)

ptr.dr_and_set(7) # I want this but with a different syntax
print(n) 