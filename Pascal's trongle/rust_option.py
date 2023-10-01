from abc import ABC, abstractmethod

class Option(ABC):

    @abstractmethod
    def unwrap(self):
        pass

class OpSome(Option):
    def __init__(self, value):
        self.value = value

    def unwrap(self):
        return self.value

class OpNone(Option):
    
    def unwrap(self):
        raise Exception("no can't unwrap a None value, stupid")
    

num = OpSome(5)
no_num = OpNone()

print(num.unwrap())
print(no_num.unwrap())