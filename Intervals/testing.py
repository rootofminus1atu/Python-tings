hi = print
print = "hi"
hi(print)

hi, print = print, "hi"



class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def tell_me_who_you_are(self):
        print("I am a rectangle.")

    def get_area(self):
        area = self.width * self.height
        return area