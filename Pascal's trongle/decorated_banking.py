
def pin_checker(func):

    def wrapper(self, *args, **kwargs):
        tries = 3

        for i in range(tries):
            inputPIN = int(input("Enter PIN: "))
            if inputPIN == self.PIN:
                print("PIN accepted")
                return func(self, *args, **kwargs)
            else:
                print(f"Incorrect PIN ({tries - i - 1} tries left)")

        print("Out of tries")

    return wrapper


# how do I include the decorator inside of the BankAccount class
# and how to get rid of self


class BankAccount:
    def __init__(self, balance, PIN):
        self.balance = balance
        self.PIN = PIN

    @pin_checker
    def check_balance(self):
        print(f"Your current balance is {self.balance}")

    @pin_checker
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrawal of {amount} successful, your new balance is {self.balance}")
        else:
            print("Insufficient funds")

    def lodge(self, amount):
        self.balance += amount
        print(f"Lodgement of {amount} successful, your new balance is {self.balance}")
