sheep = {}

class Var:
    counter = 100
    
    def __init__(self, var):
        self.var = var
        self.addr = Var.counter
        sheep[self.addr] = var
        Var.counter += 8
        
    def __repr__(self):
        return f"Var({self.var}, {self.addr})"
    
    def dereference(self):
        pass
        
n = Var(6)
print(n)

ptr = Var(n.addr)
print(ptr)


class OtherUniverse:
    sheep = {}
    counter = 100
    
    def put(self, var):
        addr = OtherUniverse.counter
        OtherUniverse.sheep[addr] = var
        OtherUniverse.counter += 8
        return var
    
    
    """  
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value"""

bog = OtherUniverse()
n = bog.put(6)
print(bog.sheep)  # Output: {100: 6}
n = 7
print(bog.sheep)  # DESIRED Output: {100: 7}

        
        
