
class Animal:
    def __init__(self, species):
        self.species = species

    def __str__(self):
        return f"This is a {self.species}"


class Mammal(Animal):
    def __init__(self):
        super().__init__("Mammal")

    def give_birth(self):
        return Mammal()


class Bird(Animal):

    def __init__(self):
        super().__init__("Bird")

    def lay_egg(self):
        return Bird()


class Fish(Animal):

        def __init__(self):
            super().__init__("Fish")

        def lay_eggs(self):
            return [Fish() for _ in range(10)]


mammal = Mammal()
print(mammal)
print(mammal.give_birth())

bird = Bird()
print(bird)
print(bird.lay_egg())

fish = Fish()
print(fish)
print(fish.lay_eggs())