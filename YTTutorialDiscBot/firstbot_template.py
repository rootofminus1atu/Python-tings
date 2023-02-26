import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()


# not sure why I'd ever use this template but whatever


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

    print(f'{username}: {user_message} ({channel})')  # chat logs

    if message.author == client.user:  # so that the bot wouldn't reply to itself to infinity
        return

    if message.channel.name == 'bot-commands':
        if user_message.lower() == 'hello':
            await message.channel.send(f'Oh hello')
            return

        if user_message.lower() == 'bye':
            await message.channel.send(f'Goodbye')
            return

    if user_message.lower() == '!anywhere':
        await message.channel.send('This can be used anywhere!')
        return


client.run(TOKEN)
