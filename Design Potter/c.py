# hidden implementation stuff
class Cell:
    def __init__(self, value, address):
        self.value = value
        self.address = address
        
class Value:
    def __init__(self, value):
        self.value = value

class Address:
    def __init__(self, address):
        self.address = address
        
# user defined stuff
def square(n):
    return n**2

var = Cell(Value(3), Address(400))
squared = square(var)  # this should return Cell(Value(9), Address(408))