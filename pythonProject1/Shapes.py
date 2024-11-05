
import math


class Shape:
    def __init__(self):
        pass

    def area(self):
        pass

    def perimeter(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius

    def area(self):
        return math.pi * self.radius * self.radius

    def perimeter(self):
        return 2 * math.pi * self.radius


class Rectangle(Shape):

    def __init__(self, length, width):
        super().__init__()
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


class Triangle(Shape):

    def __init__(self, a, b, c):
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c

print("===Circle===")
circle = Circle(5)
print(circle.area())
print(circle.perimeter())

print("===Rectangle===")
rectangle = Rectangle(5, 10)
print(rectangle.area())
print(rectangle.perimeter())

print("===Triangle===")
triangle = Triangle(3, 4, 5)
print(triangle.area())
print(triangle.perimeter())
