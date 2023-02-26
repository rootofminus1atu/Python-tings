import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View
import random
import re
import inflect
import os
from dotenv import load_dotenv
load_dotenv()
p = inflect.engine()


# hmm I was doing something here but I forgor what


bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


win_msgs = {
    0: "you won nothing",
    1: "not bad",
    2: "that's pretty good",
    3: "wow!",
}


highest_num = 4  # the highest num that can be randomized
how_many = 4     # how many numbers will be randomized
@bot.tree.command(name="lotto", description=f"guess some numbers and win")
@app_commands.describe(guess=f"Type HELP for help!")
async def lotto(interaction: discord.Interaction, guess: str):

    # picking the random numbers
    li = range(1, highest_num + 1)
    secrets = list(map(str, random.sample(li, how_many)))

    # help message
    if guess.lower() == "help":
        embed = discord.Embed(
            title="Lotto help:",
            description=f"""guess {how_many} numbers
separate them with spaces
the highest number is {highest_num}""",
            color=0x000000)
        embed.add_field(
            name="Example:",
            value=f"{' '.join(secrets)}")

        await interaction.response.send_message(embed=embed)
        return

    # formatting the user's input
    def str_to_list_and_cut(original_string, cut):
        final_list = []
        unique_set = set()

        for match in re.finditer(r'\d+', original_string):
            if match.group() not in unique_set:
                final_list.append(match.group())
                unique_set.add(match.group())

        return final_list[:cut]
    guesses = str_to_list_and_cut(guess, how_many)

    correct_guesses = []

    # check if there were correct guesses
    for num in guesses:
        if num in secrets:
            correct_guesses.append(num)

    score = len(correct_guesses)

    # the embed message
    embed = discord.Embed(
        title="Lotto result:",
        description=win_msgs[score] if score in win_msgs else "The owner forgor to add a win message :(",
        color=0x000000)
    embed.add_field(
        name="The secret numbers were...",
        value=', '.join(secrets),
        inline=False)
    embed.add_field(
        name=f"You guessed {score} numbers correctly:",
        value=', '.join(correct_guesses),
        inline=False)
    embed.add_field(
        name=f"Your guesses:",
        value=', '.join(guesses),
        inline=False)
    if score == how_many:
        embed.set_image(url="https://tenor.com/view/epic-win-gif-18390652")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="embeded", description="test")
async def embeded(interaction: discord.Interaction):
    link = "https://cdn.discordapp.com/attachments/1020719369862516818/1067204959277420575/tanaradoublechocolatebbaf58.mp4"

    embed = discord.Embed(
        title="Lotto result:",
        description="special fancy message with emojis etc",
        color=0x000000)
    embed.add_field(
        name="The secret numbers were...",
        value="the nums",
        inline=False)
    embed.add_field(
        name="You guessed X numbers correctly:",
        value="nums here",
        inline=False)

    await interaction.response.send_message(embed=embed)


bot.run(os.getenv('bot_key'))
