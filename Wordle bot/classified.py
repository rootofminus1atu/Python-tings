
def conv_func_conv(dict, func, *args):
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

    def __str__(self):
        return str((self.char, self.color))


class Keyboard:
    def __init__(self):
        keyboard_letters = "qwertyuiopasdfghjklzxcvbnm"
        self.keys = {}
        for letter in keyboard_letters:
            self.keys[letter] = "white"

    def __str__(self):
        return str(self.keys)

    def __getitem__(self, key):
        return self.keys[key]

    def __setitem__(self, key, value):
        self.keys[key] = value

    def update_keyboard(self, guess, secret):
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
        self.letters = []
        for i in range(len(input)):
            self.letters.append(Letter(input[i], "gray"))

    def __str__(self):
        return str([(letter.char, letter.color) for letter in self.letters])

    def check_word(self, secret):
        # check word
        pass


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

    def __str__(self):
        output = ""
        for row in self.rows:
            output += f"{row.word} by {row.user} +{row.points}\n"
        return output


class Wordle:
    def __init__(self):
        self.display = Display()
        self.keyboard = Keyboard()
        # and other possible additional properties

    def randomize_word(self):
        # api to pick a random word
        pass

    def play(self):
        # randomize a word
        secret = "there"

        for i in range(tries):
            # send embed with current progress (or 0 progress at the  beginning
            print(self.display)
            print(self.keyboard)

            guess = input("\nGive me a word: ")
            # god I hate oop
            # reminer to change word to not word or something
            # cuz then
            # the win condition won't work

            # guess.check_word()
            # get user ID
            # get points

            self.display.add_row(Row(Word(guess), 999, 0))

            # check keyboard
            self.keyboard.update_keyboard(guess, secret)

            if guess == secret:
                win = True
                break

        if win is True:
            print("you won")
            # send win embed
        else:
            print("rip")
            # send lose embed

hello = Word("hello")
there = Word("there")

display = Display()
display.add_row(Row(hello, 999, 2))
display.add_row(Row(there, 999, 0))
print(display.rows[1].word.letters[0].color)
print(display)

game = Wordle()
game.play()