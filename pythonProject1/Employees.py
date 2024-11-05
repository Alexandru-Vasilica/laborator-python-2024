
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary



class Engineer(Employee):
    def __init__(self, name, salary):
        super().__init__(name, salary)

    def get_raise(self):
        self.salary += 10000
        return self.salary

    def __str__(self):
        return f"Engineer: {self.name}, Salary: {self.salary}"

class Salesperson(Employee):
    def __init__(self, name, salary):
        super().__init__(name, salary)

    def make_sale(self):
        self.salary += 5000
        return self.salary

    def __str__(self):
        return f"Salesperson: {self.name}, Salary: {self.salary}"


class Manager(Employee):
    def __init__(self, name, salary):
        super().__init__(name, salary)

    def hire(self,name):
        return Engineer(name, 60000)

    def grant_raise(self,engineer):
        return engineer.get_raise()

    def __str__(self):
        return f"Manager: {self.name}, Salary: {self.salary}"


manager = Manager("John", 80000)
print(manager)
engineer = manager.hire("Jane")
print(engineer)
manager.grant_raise(engineer)
print(engineer)
salesperson = Salesperson("Tom", 40000)
salesperson.make_sale()
print(salesperson)


