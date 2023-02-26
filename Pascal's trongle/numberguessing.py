import random

# guess a number!

key = random.randint(1, 10)
print(f"\nPsst! the secret number is {key} (only for testing purposes smh)\n")

print("guess a number from 1 to 10")

for i in range(3):
    guess = int(input(f"Guess number {i+1}: "))
    if guess == key:
        print("You won!")
        break
    print("Nope :(")
