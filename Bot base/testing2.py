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
    def __init__(self, field: str):
        lower_closed, lower_num, upper_num, upper_closed = self.parse(field)
        self.field = field
        self.lower_closed = lower_closed
        self.lower_num = lower_num
        self.upper_num = upper_num
        self.upper_closed = upper_closed

    def __repr__(self) -> str:
        return f"Interval(lower_closed={self.lower_closed}, lower_num={self.lower_num}, upper_num={self.upper_num}, upper_closed={self.upper_closed})"
    
    def __contains__(self, value: float) -> bool:
        lower_check = self.lower_num <= value if self.lower_closed else self.lower_num < value
        upper_check = value <= self.upper_num if self.upper_closed else value < self.upper_num

        return lower_check and upper_check

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

class IntervalMap:
    def __init__(self, values: dict = None, not_found_case=None):
        self.data = {Interval(key): value for key, value in values.items()}
        self.not_found_case = not_found_case

    def __repr__(self) -> str:
        return f"<IntervalMap {'{'}{', '.join(f'{interval.field}: {value}' for interval, value in self.data.items())}{'}'}>"
    
    def values(self) -> list:
        return list(self.data.values())
    
    def __getitem__(self, key: float) -> Any:
        for interval, value in self.data.items():
            if key in interval:
                return value

        return self.not_found_case
    
    def slide(self, key: float) -> Any:
        for interval, value in self.data.items():
            if key in interval:
                return value

        return self.not_found_case
    

    


interval = Interval("(-10, 6]")

m2 = IntervalMap({
    "(-inf, 1)": "cold",
    "[1, 15)": "medium",
    "[15, inf)": "hot"
}, not_found_case="not found")

print(m2)
print(m2.slide(6))
print(m2[5])

