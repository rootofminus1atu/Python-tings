from dataclasses import dataclass

@dataclass(frozen=True)
class BoundaryValue:
    """
    A class that represents a boundary value of an interval. 
    
    For example, in the interval `(1, 2]`, `1` is the lower boundary value and `2` is the upper boundary value.
    """
    number: float
    closed: bool

    @property
    def open(self):
        return not self.closed
    
    def __lt__(self, other):
        if not isinstance(other, BoundaryValue):
            raise TypeError(f"Expected BoundaryValue, got {type(other)}.")
        
        if self.number != other.number:
            return self.number < other.number
        
        if self.closed and other.open:
            return False
        elif self.open and other.closed:
            return True
        else:
            return False
        
    def __le__(self, other):
        if not isinstance(other, BoundaryValue):
            raise TypeError(f"Expected BoundaryValue, got {type(other)}.")
        
        if self.number != other.number:
            return self.number <= other.number
        
        if self.closed and other.open:
            return False
        elif self.open and other.closed:
            return True
        else:
            return True
        
    def __gt__(self, other):
        if not isinstance(other, BoundaryValue):
            raise TypeError(f"Expected BoundaryValue, got {type(other)}.")
        
        if self.number != other.number:
            return self.number > other.number
        
        if self.closed and other.open:
            return True
        elif self.open and other.closed:
            return False
        else:
            return False
        
    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other
        
    def other_gt(self, other):
        return not self <= other
    

    
    def get_bracket_upper(self):
        return "]" if self.closed else ")"
    
    def get_bracket_lower(self):
        return "[" if self.closed else "("


bw1 = BoundaryValue(2, closed=True)
bw2 = BoundaryValue(3, closed=True)
print(bw1 > bw2)
print(bw1.other_gt(bw2))