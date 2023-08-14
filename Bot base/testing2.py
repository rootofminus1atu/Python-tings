from typing import Dict, Any
import re
    
class RangeMapKeyInvalid(Exception):
    pass

class RangeMapKey:
    def __init__(self, field: str):
        self.validate(field)
        self.field = field

    def __repr__(self) -> str:
        return f"<RangeMapKey field={self.field}>"
    
    def validate(self, field: str) -> None:
        pattern = r"^(-?\d*\.?\d+)?_(-?\d*\.?\d+)?$"  # Matches 'min_max', '_max', 'min_' or '_'

        if re.match(pattern, field) is not None:
            raise ValueError(f"'{field}' is not a valid RangeMapKey. Must be in format 'min_max', '_max', 'min_' or '_'.")
        
        first, second = field.split("_")

        if int(first) > int(second):
            raise ValueError(f"'{field}' is not a valid RangeMapKey. First value must be less than second value.")


class RangeMap(Dict):
    def __init__(self, values: dict = None):
        self.values = {RangeMapKey(key): value for key, value in values.items()}

    def __repr__(self) -> str:
        return f"<RangeMap values={self.values}>"

"""
m1 = RangeMap({
    "_1": "cold",
    "1_15": "medium",
    "15_": "hot"
})


print(m1)
# print(m1["_1"])

"""








class InvervalInvalid(Exception):
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
        lower_closed, lower_num, upper_num, upper_closed = self.parse(field)
        self.field = field
        self.lower_closed = lower_closed
        self.lower_num = lower_num
        self.upper_num = upper_num
        self.upper_closed = upper_closed

    def __repr__(self) -> str:
        return f"Interval(lower_closed={self.lower_closed}, lower_num={self.lower_num}, upper_num={self.upper_num}, upper_closed={self.upper_closed})"
    
    def __str__(self) -> str:
        return self.field

    def __contains__(self, value: float) -> bool:
        lower_check = self.lower_num <= value if self.lower_closed else self.lower_num < value
        upper_check = value <= self.upper_num if self.upper_closed else value < self.upper_num

        return lower_check and upper_check
    
    def __eq__(self, other):
        if isinstance(other, Interval):
            return (
                self.lower_closed == other.lower_closed and
                self.lower_num == other.lower_num and
                self.upper_num == other.upper_num and
                self.upper_closed == other.upper_closed
            )
        return False

    def __hash__(self):
        return hash((self.lower_closed, self.lower_num, self.upper_num, self.upper_closed))

    def validate(self, field: str) -> None:
        real_num = r"-?\d*\.?\d+"
        pos_inf = r"(inf)"
        neg_inf = r"(-inf)"
        left_bracket = r"(\[|\()"
        right_bracket = r"(\]|\))"

        pattern_str = rf"^\s*{left_bracket}\s*({neg_inf}|{real_num})\s*,\s*({real_num}|{pos_inf})\s*{right_bracket}\s*$"
        pattern = re.compile(pattern_str, re.IGNORECASE)

        if re.match(pattern, field) is None:
            raise InvervalInvalid(f"'{field}' is not a valid Interval. Must be in format '[min, max]', '[min, max)', '(min, max]' or '(min, max)'.")

    def parse(self, field: str) -> tuple[bool, float, float, bool]:
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
        lower = float(left_num)
        upper = float(right_num)

        if lower > upper:
            raise InvervalInvalid(f"'{field}' is not a valid Interval. First value must be less than second value.")

        return lower_closed, lower, upper, upper_closed
    
    @staticmethod
    def have_overlap(first: 'Interval', second: 'Interval') -> bool:
        """
        Returns True if the two intervals have an overlap, False otherwise.
        """
        if not isinstance(first, Interval) or not isinstance(second, Interval):
            raise TypeError(f"Incorrect types for arguments. Expected Interval, got {type(first)} and {type(second)}.")
        
        if first.upper_num < second.lower_num:
            return False

        if second.upper_num < first.lower_num:
            return False

        if first.upper_num == second.lower_num and (not first.upper_closed or not second.lower_closed):
            return False

        if second.upper_num == first.lower_num and (not second.upper_closed or not first.lower_closed):
            return False

        return True



    @staticmethod
    def are_disjoint(first: 'Interval', second: 'Interval') -> bool:
        """
        Returns True if the two intervals are disjoint, False otherwise.
        """
        if not isinstance(first, Interval) or not isinstance(second, Interval):
            raise TypeError(f"Incorrect types for arguments. Expected Interval, got {type(first)} and {type(second)}.")
        
        # disjoint calculations
        # Case 1: The upper bound of the first interval is less than the lower bound of the second interval
        if first.upper_num < second.lower_num:
            return True
        
        # Case 2: The lower bound of the first interval is greater than the upper bound of the second interval
        if first.lower_num > second.upper_num:
            return True
        
        # Case 3: The upper bound of the first interval is equal to the lower bound of the second interval,
        # and at least one of them is not closed
        if first.upper_num == second.lower_num and (not first.upper_closed or not second.lower_closed):
            return True
        
        # Case 4: The lower bound of the first interval is equal to the upper bound of the second interval,
        # and at least one of them is not closed
        if first.lower_num == second.upper_num and (not first.lower_closed or not second.upper_closed):
            return True
        
        # If none of the disjoint cases are met, the intervals must overlap
        return False
        




    def is_overlapping_with(self, other: 'Interval') -> bool:
        """
        Returns True if the two intervals intersect, False otherwise.
        """
        if not isinstance(other, Interval):
            raise TypeError(f"Cannot compare Interval with {type(other)}.")

        # overlap calculations
        so = self.__singular_overlap(other)
        co = self.__continuous_overlap(other)

        return so or co


    @staticmethod
    def __order_in_lower_starting(first: 'Interval', second: 'Interval') -> tuple['Interval', 'Interval']:
        """
        Returns the first and second interval based on the lower numbers of the intervals. 

        E. g. if `first` is `(2, 4)` and `second` is `(1, 3)`, the method will return `((1, 3), (2, 4))`.
        """

        # change for more isinstance things
        if not isinstance(first, Interval) or not isinstance(second, Interval):
            raise TypeError(f"Incorrect types for arguments. Expected Interval, got {type(first)} and {type(second)}.")
        
        if first.lower_num < second.lower_num:
            return first, second
        elif first.lower_num > second.lower_num:
            return second, first
        
        if first.lower_closed and not second.lower_closed:
            return first, second
        elif not first.lower_closed and second.lower_closed:
            return second, first
        
        # case when they start at the same number and have the same lower_closed
        return first, second

    def __singular_overlap(self, other: 'Interval') -> bool:
        """
        Returns True if the two intervals have a singular overlap, False otherwise.
        """
        if not isinstance(other, Interval):
            raise TypeError(f"Cannot compare Interval with {type(other)}.")
        
        # possibly other calculations for which one is "first" and which one is "second"
        first, second = self.__order_in_lower_starting(self, other)

        # overlap calculations

    def __continuous_overlap(self, other: 'Interval') -> bool:
        """
        Returns True if the two intervals have a continuous overlap, False otherwise.
        """
        if not isinstance(other, Interval):
            raise TypeError(f"Cannot compare Interval with {type(other)}.")
        
        # possibly other calculations for which one is "first" and which one is "second"
        first, second = self.__order_in_lower_starting(self, other)

        # overlap calculations


class OverlappingIntervalsError(Exception):
    pass

class AnotherIntervalMap(dict):
    def __init__(self, data: dict[Interval, any], not_found_case=None):
        self.check_for_overlaps(data)
        super().__init__(data)
        self.not_found_case = not_found_case

    def __repr__(self):
        the_dict = {str(interval): value for interval, value in self.items()}
        return f"<AnotherIntervalMap {the_dict}>"
    
    def slide(self, num: float) -> Any:
        for interval, value in self.items():
            if num in interval:
                return value
            
        return self.not_found_case
    
    def check_for_overlaps(self, data: dict[Interval, any]) -> None:
        """
        A helper method that checks if there are any overlapping intervals in the data.

        The current implementation works only with connected intervals, for example `(1, 2]` or `(-inf, -5)`.
        """
        intervals = list(data.keys())

        for i in range(len(intervals)):
            first = intervals[i]
            second = intervals[i + 1] if i + 1 < len(intervals) else None

            if second is None:
                break

            singular_overlap = first.upper_num == second.lower_num and (first.upper_closed and second.lower_closed)  # e.g. (1, 2] and [2, 3)
            continuous_overlap = first.upper_num > second.lower_num  # e.g. (1, 3) and (2, 4)

            if singular_overlap or continuous_overlap:
                raise OverlappingIntervalsError(f"Intervals {str(first)} and {str(second)} overlap. Overlapping intervals are not allowed.")


mp = {
    Interval("(-inf, 1)"): "cold",
    Interval("[1, 15)"): "medium",
    Interval("[15, 30)"): "hot"
}
mp[Interval("[30, inf)")] = "very hot"

m3 = AnotherIntervalMap(mp, not_found_case="not found")

print(m3)

m3.pop(Interval("[1, 15)"))

print(m3)


test_itvs = [
    (Interval("(-inf, 2)"), Interval("(1, 3)")),
    (Interval("(-inf, 2)"), Interval("(2, 3)")),
    (Interval("[1, 2)"), Interval("(0, 1]"))
]

for first, second in test_itvs:
    print("first:", first)
    print("second:", second)
    print("Have overlap:", Interval.have_overlap(first, second))
    print("=====================================")

