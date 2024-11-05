
class Account:
    def __init__(self, account_holder, account_balance):
        self.account_holder = account_holder
        self.account_balance = account_balance

    def deposit(self, amount):
        self.account_balance += amount

    def get_balance(self):
        return self.account_balance

    def calculate_interest(self):
        pass

    def withdraw(self, amount):
        if self.account_balance < amount:
            return "Insufficient balance"
        else:
            self.account_balance -= amount


class SavingsAccount(Account):
    def __init__(self, account_holder, account_balance, interest_rate):
        super().__init__(account_holder, account_balance)
        self.interest_rate = interest_rate

    def calculate_interest(self, years):
        total = self.account_balance
        for i in range(years):
            total += total * self.interest_rate
        return total - self.account_balance


class CheckingAccount(Account):
    def __init__(self, account_holder, account_balance, fee):
        super().__init__(account_holder, account_balance)
        self.fee = fee

    def withdraw(self, amount):
        if self.account_balance < amount + self.fee:
            return "Insufficient balance"
        else:
            self.account_balance -= amount + self.fee
            return self.account_balance


savings = SavingsAccount("John", 1000, 0.05)
print(savings.calculate_interest(5))


checking = CheckingAccount("Jane", 1000, 10)
checking.withdraw(100)
print(checking.get_balance())



