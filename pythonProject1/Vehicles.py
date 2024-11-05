
CURRENT_YEAR = 2024


class Vehicle:
    def __init__(self, maker, model, year,miles_per_year,towing_capacity):
        self.maker = maker
        self.model = model
        self.year = year
        self.miles_per_year = miles_per_year
        self.towing_capacity = towing_capacity

    def get_mileage(self):
        return (CURRENT_YEAR - self.year) * self.miles_per_year

    def get_towing_capacity(self):
        return self.towing_capacity


class Car(Vehicle):
    def __init__(self, maker, model, year):
        super().__init__(maker, model, year, 15000, 200)


class Motorcycle(Vehicle):
    def __init__(self, maker, model, year):
        super().__init__(maker, model, year, 5000, 20)


class Truck(Vehicle):
    def __init__(self, maker, model, year):
        super().__init__(maker, model, year, 30000, 700)


print("===Car===")
car = Car("Toyota", "Corolla", 2018)
print(car.get_mileage())
print(car.get_towing_capacity())

print("===Motorcycle===")
motorcycle = Motorcycle("Honda", "F", 2019)
print(motorcycle.get_mileage())
print(motorcycle.get_towing_capacity())

print("===Truck===")
truck = Truck("Ford", "T", 2015)
print(truck.get_mileage())
print(truck.get_towing_capacity())



