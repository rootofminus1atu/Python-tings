from typing import Dict, Any, Optional
import re
from dataclasses import dataclass

# TODO:
# - better error messages with regex
# - disjoint intervals? maybe?


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
        
        if self.open and other.closed:
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
        else:
            return True
        
    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other
    

    def get_bracket_upper(self) -> str:
        """
        Returns the bracket that should be used for the upper boundary value. 
        So if the boundary value is closed, it returns `"]"`, if it's open it returns `")"`.
        """
        return "]" if self.closed else ")"
    
    def get_bracket_lower(self) -> str:
        """
        Returns the bracket that should be used for the upper boundary value. 
        So if the boundary value is closed, it returns `"["`, if it's open it returns `"("`.
        """
        return "[" if self.closed else "("



class IvalidIntervalError(Exception):
    pass

class Interval:
    """
    A class that represents intervals.

    The intervals defined with this class are connected and continuous, for example `(1, 2]` or `(-inf, -5)`. 
    Disjoint intervals are not supported.
    Interval operations like `(1, 3) u (2, 4)` or `[1, 4] \ (2, 3)` are not supported either. 
    
    Singletons like `{1}` are supported, however you must write them down like `[1, 1]`.
    """
    def __init__(self, field: str):
        lower_closed, lower_number, upper_number, upper_closed = self.parse(field)
        self.field = field
        self.lower = BoundaryValue(lower_number, lower_closed)
        self.upper = BoundaryValue(upper_number, upper_closed)

    def __repr__(self) -> str:
        return f"{self.field}"
    
    def __str__(self) -> str:
        return f"{self.field}"

    def __contains__(self, value: float) -> bool:
        lower_check = self.lower.number <= value if self.lower.closed else self.lower.number < value
        upper_check = value <= self.upper.number if self.upper.closed else value < self.upper.number

        return lower_check and upper_check
    
    def __eq__(self, other):
        if isinstance(other, Interval):
            return (
                self.lower == other.lower and
                self.upper == other.upper
            )
        return False

    def __hash__(self):
        return hash((self.lower, self.upper))
    
    def intersection(self, other: 'Interval') -> Optional['Interval']:
        """
        Returns the intersection of two intervals. If the intervals don't overlap, returns `None`.
        """
        if not isinstance(other, Interval):
            raise TypeError(f"Incorrect type for argument. Expected Interval, got {type(other)}.")
        
        first = self
        second = other

        if not first.overlaps_with(second):
            return None

        new_lower = max(first.lower, second.lower)
        new_upper = min(first.upper, second.upper)

        return Interval(f"{new_lower.get_bracket_lower()}{new_lower.number}, {new_upper.number}{new_upper.get_bracket_upper()}")

    def overlaps_with(self, other: 'Interval') -> bool:
        first = self
        second = other

        if not isinstance(first, Interval) or not isinstance(second, Interval):
            raise TypeError(f"Incorrect types for arguments. Expected Interval, got {type(first)} and {type(second)}.")

        if first.upper.number < second.lower.number:
            return False

        if second.upper.number < first.lower.number:
            return False

        if first.upper.number == second.lower.number and (first.upper.open or second.lower.open):
            return False

        if second.upper.number == first.lower.number and (second.upper.open or first.lower.open):
            return False

        return True

    def validate(self, field: str) -> None:
        real_num = r"-?\d*\.?\d+"
        pos_inf = r"\+?(inf)"
        neg_inf = r"(-inf)"
        left_bracket = r"(\[|\()"
        right_bracket = r"(\]|\))"

        pattern_str = rf"^\s*{left_bracket}\s*({neg_inf}|{real_num})\s*,\s*({real_num}|{pos_inf})\s*{right_bracket}\s*$"
        pattern = re.compile(pattern_str, re.IGNORECASE)

        if re.match(pattern, field) is None:
            raise IvalidIntervalError(f"'{field}' is not a valid Interval. Must be in format '[min, max]', '[min, max)', '(min, max]' or '(min, max)'.")

    def parse(self, field: str) -> tuple[bool, float, float, bool]:
        """
        Parses the string representation of an interval and returns a tuple of the form `(lower_closed, lower, upper, upper_closed)`.

        Before the parsing occurs, the string is validated with the `validate` method. If the string is not valid, an `IvalidIntervalError` is raised.

        Another `InvalidIntervalError` is raised if the first value is greater than the second value.
        """
        self.validate(field)

        field_stripped = field.strip()
        left_bracket = field_stripped[0]
        right_bracket = field_stripped[-1]
        insides = field_stripped[1:-1].strip()
        insides_split = insides.split(",")
        left_num = insides_split[0].strip()
        right_num = insides_split[1].strip()

        lower_closed = left_bracket == "["
        upper_closed = right_bracket == "]"

        try: 
            lower = int(left_num)
        except ValueError:
            lower = float(left_num)
        try:
            upper = int(right_num)
        except ValueError:
            upper = float(right_num)

        if lower > upper:
            raise IvalidIntervalError(f"'{field}' is not a valid Interval. First value must be less than second value.")

        return lower_closed, lower, upper, upper_closed



class OverlappingIntervalsError(Exception):
    pass

class AnotherIntervalMap(dict):
    def __init__(self, data: dict[Interval, Any], not_found_case=None):
        self.check_for_overlaps(data)
        super().__init__(data)
        self.not_found_case = not_found_case

    def __repr__(self):
        return f"<AnotherIntervalMap={super().__repr__()}, not_found_case={self.not_found_case}>"
    
    def slide(self, num: float) -> Optional[Any]:
        if not isinstance(num, float) and not isinstance(num, int):
            raise TypeError(f"Expected float, got {type(num)}.")

        for interval, value in self.items():
            if num in interval:
                return value
            
        return self.not_found_case
    
    def __setitem__(self, interval: Interval, value: Any) -> None:
        if not isinstance(interval, Interval):
            raise TypeError(f"Expected Interval, got {type(interval)}.")
        
        self.check_for_overlaps_with(interval)
        
        super().__setitem__(interval, value)
    
    def check_for_overlaps_with(self, interval: Interval) -> None:
        for itv in self.keys():
            if itv.overlaps_with(interval):
                raise OverlappingIntervalsError(f"Interval {interval} overlaps with {itv}. Overlapping intervals are not supported.")
    
    def check_for_overlaps(self, data: dict[Interval, any]) -> None:
        """
        A helper method that checks if there are any overlapping intervals in the data.

        The current implementation works in O(n^2) time.
        """
        intervals = data.keys()

        for i1 in intervals:
            for i2 in intervals:
                if i1 == i2:
                    continue

                if i1.overlaps_with(i2):
                    raise OverlappingIntervalsError(f"Intervals {i1} and {i2} overlap. Overlapping intervals are not supported.")


itv = Interval("[1, 4]")
itv2 = Interval("[2, 3]")
result = itv.intersection(itv2)
print(result)
print(itv, itv2)

print(Interval("(2, 2)"))


"""
itv = Interval("[1, inf)")
print(itv)
print(itv.lower)
print(itv.upper)
print(float("inf") in itv)
print(itv == Interval("[1, inf]"))

itv_overlap_tests = [
    ("[1, 2]", "[2, 3]", True),
    ("[1, 2]", "[1, 3]", True),
    ("[1, 2]", "[1, 2]", True),
    ("[1, 2]", "(0, 1)", False),
    ("[1, 2]", "[0, 0]", False),
    ("[1, 2)", "[0, 0.5)", False),
    ("[1, 2]", "[0, 1.5)", True),
    ("[1, 2]", "[0, 2]", True),
    ("[1, 2]", "[0, 3]", True),
    ("[1, 2]", "[1, 3]", True),
    ("[1, 2]", "[1, 2]", True),
    ("(1, 2]", "[1, 1]", False),
    ("(3, 4)"," (1, 2)", False),
    ("(3, 4)"," (2, 3)", False),
    ("[3, 4)"," (2, 3)", False),
    ("[3, 4)"," (2, 3]", True),
    ("[5, inf)"," (-inf, 2]", False),
]

for first, second, expected in itv_overlap_tests:
    first_itv = Interval(first)
    second_itv = Interval(second)
    print(first_itv, second_itv, first_itv.overlaps_with(second_itv), expected)
    print("=====================================")


mp = {
    Interval("(-inf, 1)"): "cold",
    Interval("[1, 15)"): "medium",
    Interval("[15, 30)"): "hot"
}

m3 = AnotherIntervalMap(mp, not_found_case="not found")
print(m3)
print(m3.slide(1))
m3[Interval("[30, inf)")] = "very hot"
print(m3)

"""