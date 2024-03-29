from typing import Dict, Any, Optional
import re
from dataclasses import dataclass
from enum import Enum, auto

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

class IntervalParser:
    REAL_NUM = r"-?\d*\.?\d+"
    POS_INF = r"\+?(inf)"
    NEG_INF = r"(-inf)"
    LEFT_BRACKET = r"(\[|\()"
    RIGHT_BRACKET = r"(\]|\))"

    def validate_input(self, field: str) -> None:
        pattern_str = rf"^\s*{self.LEFT_BRACKET}\s*({self.NEG_INF}|{self.REAL_NUM})\s*,\s*({self.REAL_NUM}|{self.POS_INF})\s*{self.RIGHT_BRACKET}\s*$"
        pattern = re.compile(pattern_str, re.IGNORECASE)

        if re.match(pattern, field) is None:
            raise IvalidIntervalError(f"'{field}' is not a valid Interval. Must be in format '[min, max]', '[min, max)', '(min, max]' or '(min, max)'.")
        
    def validate_data(self, first: BoundaryValue, second: BoundaryValue, field: str) -> None:
        if first.number > second.number:
            raise IvalidIntervalError(f"First value must be less than second value.")
        
        if first.number == second.number and (first.open and second.open):
            raise IvalidIntervalError(f"An interval cannot be open from both sides. (Open sets coming soon tho)")

        if first.number == second.number and (first.open or second.open):
            raise IvalidIntervalError(f"A single value cannot be both open and closed from 2 different sides.")
        

    def extract_data(self, field: str) -> tuple[str, float | int, float | int, str]:
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

        return lower_closed, lower, upper, upper_closed

    def parse(self, field: str) -> tuple[BoundaryValue, BoundaryValue]:
        self.validate_input(field)

        lower, lower_closed, upper, upper_closed = self.extract_data(field)

        first, second = BoundaryValue(lower, lower_closed), BoundaryValue(upper, upper_closed)

        try:
            self.validate_data(first, second)
        except IvalidIntervalError as e:
            raise IvalidIntervalError(f"'{field}' is not a valid Interval. {e}")

        return first, second



class Interval:
    """
    A class that represents intervals.

    The intervals defined with this class are connected and continuous, for example `(1, 2]` or `(-inf, -5)`. 
    Disjoint intervals are not supported.
    Interval operations like `(1, 3) u (2, 4)` or `[1, 4] \ (2, 3)` are not supported either. 
    
    Singletons like `{1}` are supported, however you must write them down like `[1, 1]`.
    """
    def __init__(self, field: str):
        lower, upper = IntervalParser().parse(field)
        self.field: str = field
        self.lower: BoundaryValue = lower
        self.upper: BoundaryValue = upper

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


itv = Interval("[1, inf)")
print(itv)
print(999 in itv)  # True




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

