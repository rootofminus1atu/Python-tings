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