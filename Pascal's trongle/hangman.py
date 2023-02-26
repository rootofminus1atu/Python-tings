# hangman game
import requests

baseResponse = requests.get("https://random-word-api.herokuapp.com/word").json()
word = baseResponse[0]

tries = len(word)  # 5
# word = "hello"
display = ""
wincounter = 0

for i in range(len(word)):
    display += "_"

lstword = list(word)
lstdisplay = list(display)
usedletters = []


# the part above is all setup


print(f"You have {tries} tries")

i = 0
while i < tries and wincounter < len(word):
    print(f"The letters you used so far: {', '.join(usedletters)}")
    print(' '.join(lstdisplay))

    guess = input(f"Guess number {tries - i}: ").lower()

    if len(guess) > 1:
        print("You wasted an attempt... Input 1 letter next time")

    elif guess in usedletters:
        print("You guessed that letter already :/")
        usedletters.remove(guess)
        i -= 1

    elif guess in lstword:
        while guess in lstword:
            index = lstword.index(guess)
            lstdisplay[index] = guess
            lstword[index] = 'xx'
            wincounter += 1

        i -= 1

    else:
        print("Nope")

    usedletters.append(guess)
    i += 1

print(' '.join(lstdisplay))

if wincounter == len(word):
    print("You won! :)")
else:
    print(f"You lost, The secret word was: {word}")
