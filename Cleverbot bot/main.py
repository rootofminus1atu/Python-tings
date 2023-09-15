import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

from cleverbot_final import CleverbotConversation

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.cleverbot = CleverbotConversation(max_context=100)

@bot.event
async def on_ready():
    print('Bot is ready.')



@bot.event
async def on_message(message):
    print("on message triggered")
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        cleared_message = message.content.replace(f'<@{bot.user.id}>', '').strip()

        response = await asyncio.to_thread(bot.cleverbot.respond, cleared_message)

        await message.reply(response)
        return
    
    await bot.process_commands(message)
    

@bot.command()
async def ping(ctx):
    print("ping triggered")
    await ctx.send('pong')

@bot.command(name='forget')
async def forget(ctx):
    print("forget triggered")
    bot.cleverbot.wipe_context()
    await ctx.send('Context wiped.')

bot.run(os.getenv('TOKEN'))