
def conv_func_conv(dict, func, *args):
    # conv func conv stands for:
    # convert, apply func, convert back
    inv_dict = {v: k for k, v in dict.items()}
    return inv_dict[func(*[dict[arg] for arg in args])]


color_dict = {
    "gray": -1,
    "white": 0,
    "yellow": 1,
    "green": 2
}

word_len = 5
tries = 6


class Letter:
    def __init__(self, char: str, color: str):
        self.char = char
        self.color = color

    def __repr__(self):
        return f"({self.char}, {self.color})"

    def __str__(self):
        return self.char


class Keyboard:
    def __init__(self):
        self.keyboard_letters = "qwertyuiopasdfghjklzxcvbnm"
        self.keys = {}
        for letter in self.keyboard_letters:
            self.keys[letter] = "white"

    def __repr__(self):
        return f"{self.keys}"

    def __getitem__(self, key):
        return self.keys[key]

    def __setitem__(self, key, value):
        self.keys[key] = value

    def update_keyboard(self, guess: str, secret: str):
        for i in range(len(guess)):
            if guess[i] == secret[i]:
                self[guess[i]] = conv_func_conv(color_dict, max, self[guess[i]], "green")
            elif guess[i] in secret:
                self[guess[i]] = conv_func_conv(color_dict, max, self[guess[i]], "yellow")
            else:
                self[guess[i]] = "gray"

    def update_keyboard2(self, guess, secret):
        for i in range(len(guess.letters)):
            if guess.letters[i].char == secret[i]:
                self[guess.letters[i].char] = conv_func_conv(color_dict, max, self[guess.letters[i].char], "green")

        for i in range(len(guess.letters)):
            if guess.letters[i].char in secret:
                self[guess.letters[i].char] = conv_func_conv(color_dict, max, self[guess.letters[i].char], "yellow")

        for letter in guess.letters:
            if letter.char not in secret:
                self[letter.char] = "gray"


class Word:
    def __init__(self, input: str):
        self.letters = [Letter(cha, "gray") for cha in input]

    def __repr__(self):
        return f"{[(letter.char, letter.color) for letter in self.letters]}"
    
    def __str__(self):
        return ''.join([letter.char for letter in self.letters])

    def check_word(self, secret: str):
        secret_temp = list(str(secret))
        guess_temp = list(str(self))

        # check which letters should be highlighted GREEN
        for i, cha in enumerate(guess_temp):
            if cha == secret_temp[i]:
                self.letters[i].color = "green"
                secret_temp[i] = '*'
                guess_temp[i] = '*'

        # check which letters should be highlighted YELLOW
        for i, cha in enumerate(guess_temp):
            if cha in secret_temp and cha != "*":
                self.letters[i].color = "yellow"
                secret_temp[secret_temp.index(cha)] = '*'
                guess_temp[guess_temp.index(cha)] = '*'

        return self


class Row:
    def __init__(self, word: Word, user: int, points: int):
        self.word = word
        self.user = user
        self.points = points


class Display:
    def __init__(self):
        self.rows = []

    def add_row(self, row: Row):
        self.rows.append(row)

    def __repr__(self):
        output = ""
        for row in self.rows:
            output += f"{repr(row.word)} by {row.user} +{row.points}\n"
        return output

    def calculate_points(self, guess: Word):
        # I have to add some logic for yellow points too

        total = 0
        for i, lettr in enumerate(guess.letters):
            if lettr.color == "green":

                for row in self.rows:
                    if row.word.letters[i].color == "green":
                        total -= 2
                        break

                total += 2

        return total


class Wordle:
    def __init__(self, secret: str):
        self.display = Display()
        self.keyboard = Keyboard()
        self.secret = secret
        self.won = False
        # and other possible additional properties

    def attempt(self, guess: str):
        # check word
        # get user ID
        # get points
        guess_checked = Word(guess).check_word(self.secret)
        user_id = 999
        points = self.display.calculate_points(guess_checked)

        self.display.add_row(Row(
            word=guess_checked,
            user=user_id,
            points=points)
        )

        # check keyboard
        self.keyboard.update_keyboard(guess, self.secret)

        if guess == self.secret:
            self.won = True

    def console_play(self):
        for i in range(tries):
            # send embed with current progress (or 0 progress at the  beginning
            print(self.display)
            print(self.keyboard)

            guess = input("\nGive me a word: ")
            
            self.attempt(guess)

            if self.won is True:
                break

        print(self.display)
        print(self.keyboard)
        
        if self.won is True:
            print("you won")
            # send win embed
        else:
            print("rip")
            # send lose embed
            
    def discord_play(self):
        pass
"""
hello = Word("hello")
there = Word("there")

display = Display()
display.add_row(Row(hello, 999, 2))
display.add_row(Row(there, 999, 0))
print(display.rows[1].word.letters[0].color)
print(display)"""


# the secret word can be randomized outside
# or inside idk
game = Wordle("there")
game.play()