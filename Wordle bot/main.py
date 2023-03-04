import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")




# check if a number is non-negative
def is_non_negative(num):
    return num >= 0

# to calculate points
# except it doesn't calculate them correctly... yet=
def calculate_points(before, after):
    return sum(filter(is_non_negative, map(lambda x: color_dict2[x], after.values()))) - sum(filter(is_non_negative, map(lambda x: color_dict2[x], before.values())))


# convert using a dict, apply a function, convert back
# useful when you want to determine what's bigger, "yellow" or "green"
def conv_func_conv(dict, func, *args):
    inv_dict = {v: k for k, v in dict.items()}
    return inv_dict[func(*[dict[arg] for arg in args])]

color_dict = {
    -1: "gray",
    0: "white",
    1: "yellow",
    2: "green"
}

color_dict2 = {
    "gray": -1,
    "white": 0,
    "yellow": 1,
    "green": 2
}


@bot.command()
async def wordle2(ctx):
    secret = "eeeggg"
    tries = 8
    win = False
    data = []
    keyboard = {char: "white" for char in "qwertyuiopasdfghjklzxcvbnm"}
    guesser = []

    # game start
    for attempt in range(tries):
        await ctx.send(f"Attempt number {attempt + 1}: ")

        # input word and input user
        guess = ""
        while len(guess) != len(secret) or not guess.isalpha():
            guess = await bot.wait_for('message')
            guesser_id = guess.author.id
            guess = guess.content.lower()


        # temp data for 1 word
        guess_data = [(char, "gray") for char in guess]
        keyboard_before = keyboard.copy()
        secret_temp = list(secret)
        guess_temp = list(guess)

        print(f"secret temp: {secret_temp}")
        print(f"guess temp: {guess_temp}")

        # check which letters should be highlighted GREEN
        for i in range(len(guess_temp)):
            if guess_temp[i] == secret_temp[i]:
                guess_data[i] = (guess[i], "green")
                keyboard[guess[i]] = conv_func_conv(color_dict2, max, keyboard[guess[i]], "green")
                # the stars below are like a reservation
                # if a green letter is detected, its place is reserved by the star
                # and because of that the yellow letters at the next step won't have access to it
                #
                # this kind of thing is necessary in case of duplicated letters
                # and a similar procedure is used for the yellow letters
                secret_temp[i] = '*'
                guess_temp[i] = '*'

        print(f"secret temp: {secret_temp}")
        print(f"guess temp: {guess_temp}")

        # check which letters should be highlighted YELLOW
        for i in range(len(guess_temp)):
            if guess_temp[i] in secret_temp and guess_temp[i] != "*":
                guess_data[i] = (guess[i], "yellow")
                keyboard[guess[i]] = conv_func_conv(color_dict2, max, keyboard[guess[i]], "yellow")
                # star character reservations again
                #
                # if you're still confused draw this case on paper:
                # secret word: EEEGGG
                # guess: EGEEGE
                #
                # if you have a better idea of how to solve proper letter highlighting just text me
                secret_temp[secret_temp.index(guess_temp[i])] = '*'
                guess_temp[guess_temp.index(guess_temp[i])] = '*'

        print(f"secret temp: {secret_temp}")
        print(f"guess temp: {guess_temp}")

        # check which letters should be highlighted GRAY on the KEYBOARD
        for letter in guess:
            if letter not in secret:
                keyboard[letter] = "gray"

        data.append(guess_data)

        keyboard_after = keyboard
        points = calculate_points(keyboard_before, keyboard_after)  # currently calculated incorrectly
        print(f"\nPOINTS: {points} (currently calculate incorrectly)\n")

        guesser.append((guesser_id, points))

        bonus = "**+2**"  # this also needs more work

        # show data in the console
        print(guess_data)
        print(data)
        print(keyboard_after)
        print(guesser)

        # show data in discord
        await ctx.send(embed=wordle_embed2(data, guesser, keyboard_after, bonus))

        # check if the user guessed the whole word
        if guess == secret:
            win = True
            break

    # won or lost?
    if win is True:
        await ctx.send("you won")
    else:
        await ctx.send("rip")


@bot.command()
async def wordle(ctx):
    secret = "aloft"
    tries = 8
    win = False
    data = []
    keyboard = {char: 0 for char in "qwertyuiopasdfghjklzxcvbnm"}
    guesser = []


    # game start
    for attempt in range(tries):
        await ctx.send(f"Attempt number {attempt + 1}: ")

        # input word and input user
        # I HAVE TO ADD BETTER WORD VALIDATION
        guess = ""
        guesser_id = ""
        while len(guess) != len(secret) or not guess.isalpha():
            guess = await bot.wait_for('message')
            guesser_id = guess.author.id
            guess = guess.content.lower()

        print(guesser_id)
        print(guess)

        # word data
        guess_data = [{char: -1} for char in guess]

        # temp info used to determine:
        # points data
        keyboard_before = keyboard.copy()
        # letter highlighting data
        secret_temp = list(secret)



        # check which letters should be highlighted GREEN
        for i in range(len(guess)):
            if guess[i] == secret_temp[i]:  # green
                guess_data[i] = {guess[i]: 2}
                keyboard[guess[i]] = max(keyboard[guess[i]], 2)
                secret_temp[i] = '*'

        # check which letters should be highlighted YELLOW
        for i in range(len(guess)):
            if guess[i] in secret_temp:  # yellow
                guess_data[i] = {guess[i]: 1}
                keyboard[guess[i]] = max(keyboard[guess[i]], 1)
                secret_temp[secret_temp.index(guess[i])] = '*'

        # check which letters should be highlighted GRAY on the KEYBOARD
        for letter in guess:
            if letter not in secret:
                keyboard[letter] = -1


        data.append(guess_data)
        keyboard_after = keyboard

        points = calculate_points(keyboard_before, keyboard_after)
        print(f"\nPOINTS: {points}\n")



        guesser.append((guesser_id, points))


        # show data in the console
        print(guess_data)
        print(data)
        print(keyboard_after)
        print(guesser)

        # show data to the user
        await ctx.send(guess_data)
        await ctx.send(data)
        await ctx.send(keyboard_after)
        await ctx.send(guesser)

        # check if the user guessed the whole word
        if guess == secret:
            win = True
            break

    # won or lost?
    if win is True:
        await ctx.send("you won")
    else:
        await ctx.send("rip")



# w2e and w3e are the ids of the servers in which I keep the emojis
# the colored letter emojis
# and I need 2 servers cuz of the 50 emoji limit (and I need around 100 for all the possible letters and colors)
w2e = 1070328477334642698
w3e = 1070328574726389792


@bot.command()
async def emoji(ctx, color: str, char: str):
    await ctx.send(get_emoji(color, char))

def get_emoji(color, char):
    emoji_name = color + "_" + char
    server_list = [w2e, w3e]

    for server_id in server_list:
        server = bot.get_guild(server_id)
        emoji = discord.utils.get(server.emojis, name=emoji_name)

        if emoji is not None:
            return str(emoji)

    return "🆘"


def wordle_embed2(data, user, keyboard, bonus):
    desc = ""
    for i in range(len(data)):
        desc += f"`{i+1}.` {''.join([get_emoji(pair[1], pair[0]) for pair in data[i]])}"
        desc += f" <@{user[i][0]}> +{user[i][1]} {bonus}\n"

    keyb = "".join([get_emoji(keyboard[char], char) for char in keyboard if char in "qwertyuiop"]) + "\n"
    keyb += "".join([get_emoji(keyboard[char], char) for char in keyboard if char in "asdfghjkl"])
    keyb += "<:gray_square:1070886986191216791>\n<:gray_square:1070886986191216791>"  # gray square
    keyb += "".join([get_emoji(keyboard[char], char) for char in keyboard if char in "zxcvbnm"])
    keyb += "<:gray_square:1070886986191216791><:gray_square:1070886986191216791>"

    embed = discord.Embed(
        title="Wordle",
        description=desc,
        color=0x000000)
    embed.add_field(
        name="",
        value="",
        inline=False)
    embed.add_field(
        name="",
        value=keyb,
        inline=False)
    embed.add_field(
        name="",
        value="",
        inline=False)
    embed.add_field(
        name="",
        value=f"you won | you ran out of guesses (this is a win msg)",
        inline=False)
    embed.add_field(
        name="",
        value="",
        inline=False)
    embed.add_field(
        name="",
        value=f"don't know how to play type `!rules` (also wip)",
        inline=False)
    return embed

def wordle_embed(data, user, keyboard, bonus):
    embed = discord.Embed(
        title="Co-ordle for this day",
        description=f"`1.` {''.join([get_emoji(color_dict[pair[1]], pair[0]) for pair in data[0]])} <@{user[0][0]}> +{user[0][1]} {bonus}",
        color=0x000000)
    embed.add_field(
        name="",
        value="",
        inline=False)
    embed.add_field(
        name="",
        value=f"keyboard",
        inline=False)
    embed.add_field(
        name="",
        value="",
        inline=False)
    embed.add_field(
        name="",
        value=f"you ran out of guesses!",
        inline=False)
    embed.add_field(
        name="",
        value="",
        inline=False)
    embed.add_field(
        name="",
        value=f"don't know how to play type rules",
        inline=False)
    return embed


# helper command
# I used it with hardcoded data to see how it'd be displayed
# if you want to experiment with it too, play a round of wordle and then paste the info somewhere above
# then use the command, and you should get an embed
@bot.command()
async def say(ctx):
    # await ctx.send(embed=wordle_embed2(data, user, keyboard, bonus))
    pass


bot.run(os.getenv('bot_key'))
