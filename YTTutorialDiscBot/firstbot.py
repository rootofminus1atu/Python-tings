import discord
import random
import math
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()


# 1st bot, not very good


TOKEN = os.getenv('bot_key')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:  # so that the bot wouldn't reply to itself to infinity
        return

    if message.channel.name == 'bot-commands':
        if user_message.lower() == 'hello':
            await message.channel.send(f'Oh hello')
            return

        elif user_message.lower() == 'how are you today':
            await message.channel.send(f"I've been better")
            return

        elif user_message.lower() == "what's the news from the other side of tamriel":
            await message.channel.send(f"Nothing I'd like to talk about")
            return

        elif user_message.lower() == 'bye':
            await message.channel.send(f'Goodbye')
            return

        elif user_message.lower() == '!d6':
            response = f'D6 roll result: {random.randint(1,6)}'
            await message.channel.send(response)
            return

        elif user_message.lower() == '!random':
            texts = ("hi there",
                     "ok",
                     "bye")

            text = random.choice(texts)
            await message.channel.send(text)
            return

        elif 'chuck norris' in user_message.lower():
            response = requests.get("https://api.chucknorris.io/jokes/random")
            print(response.status_code)
            await message.channel.send(json.dumps(response.json()["value"], indent=4))
            return

        elif user_message.lower() == '!fox':
            fox = requests.get("https://randomfox.ca/floof").json()
            await message.channel.send(fox["image"])
            return

        elif user_message.lower().split(' ')[0] == '!wiggle':
            if len(user_message.split(' ')) == 1:
                await message.channel.send(wiggle("wiggle"))
                return

            text = user_message.split(' ')[1]

            if len(wiggle(text)) > 2000:
                await message.channel.send(f"That's too long! ({len(wiggle(text))})")
                return

            if len(user_message.split(' ')) == 2:
                await message.channel.send(wiggle(text))
                return

            howmany = user_message.split(' ')[2]

            if is_pos_int(howmany) is False:
                await message.channel.send(f'"{howmany}" is not a positive integer...')
                return

            else:
                for k in range(0, int(howmany)):
                    await message.channel.send(wiggle(text))
                return

        elif user_message.lower().split(' ')[0] == '!bigwiggle':
            if len(user_message.split(' ')) == 1:
                await message.channel.send(bigwiggle("bigwiggle"))
                return

            text = user_message.split(' ')[1]

            if len(bigwiggle(text)) > 2000:
                await message.channel.send(f"That's too long! ({len(bigwiggle(text))})")
                return

            if len(user_message.split(' ')) == 2:
                await message.channel.send(bigwiggle(text))
                return

            howmany = user_message.split(' ')[2]

            if is_pos_int(howmany) is False:
                await message.channel.send(f'"{howmany}" is not a positive integer...')
                return

            else:
                for k in range(0, int(howmany)):
                    await message.channel.send(bigwiggle(text))
                return

    if user_message.lower() == '!anywhere':
        await message.channel.send('This can be used anywhere!')
        return


def wiggle(text):
    amplitude = 30
    wavelength = 20
    bumps = 2
    streeng = ""
    for i in range(bumps * wavelength):
        streeng += round(amplitude * (math.sin(math.pi/wavelength * i))**2) * " " + text + "\n"
    return streeng


def bigwiggle(text):
    amplitude = 60
    wavelength = 50
    bumps = 1
    streeng = ""
    for i in range(bumps * wavelength):
        streeng += round(amplitude * (math.sin(math.pi/wavelength * i))**2) * " " + text + "\n"
    return streeng


def is_pos_int(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        if float(n) < 1:
            return False
        else:
            return float(n).is_integer()


client.run(TOKEN)
