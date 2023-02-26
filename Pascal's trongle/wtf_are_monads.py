import inspect

class Box:
    def __init__(self, weight):
        self.weight = weight

    def show(self):
        print(f"My weight is {self.weight}")

    def double(self, box):
        self.weight = 2*self.weight
        return Box(self.weight)

    def apply(self, func):
        weight_after = func(self.weight)
        return Box(weight_after)


mybox = Box(40)
mybox.show()

def double(n):
    return Box(2*n)

mybox1 = mybox.apply(double)
mybox1.show()

mybox2 = mybox.apply(double.apply(double))
mybox2.show()
