import random
import re

# co-ordle

# v1 but even worse
# no white chars for the keyboard

color_dict = {
    0: "gray",
    1: "yellow",
    2: "green"
}

secret = list("apple")
secret_temp = secret.copy()
tries = 8

win = False
data = []


keyboard = {char: 0 for char in "qwertyuiopasdfghjklzxcvbnm"}


for attempt in range(tries):
    print(f"Attempt number {attempt + 1}: ")

    guess = ""
    while len(guess) != len(secret):
        guess = input("type a word")

    guess_data = []
    keyboard_before = keyboard.copy()


    # fuck me
    # I have to change so much
    # too much
    # sdfpjasjasofhoasklfhalkhsf
    for i in range(len(guess)):
        if guess[i] == secret_temp[i]:  # green
            guess_data.append((guess[i], 2))
            keyboard[guess[i]] = max(keyboard[guess[i]], 2)
            secret_temp[i] = '*'

        elif guess[i] in secret_temp:  # yellow
            guess_data.append((guess[i], 1))
            keyboard[guess[i]] = max(keyboard[guess[i]], 1)
            secret_temp[i] = '*'

        else:                      # grey
            guess_data.append((guess[i], 0))



    keyboard_after = keyboard
    data.append(guess_data)
    print(guess_data)
    print(data)

    print(keyboard_before)
    print(keyboard_after)

    def non_negative(num):
        if num >= 0:
            return True
        return False

    points = sum(filter(non_negative, keyboard_after.values())) - sum(filter(non_negative, keyboard_before.values()))
    print(f"\nPOINTS: {points}\n")

    if guess == secret:
        win = True
        break


if win is True:
    print("you won")
else:
    print("rip")
