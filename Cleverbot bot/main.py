import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import aiosqlite
import asyncio
load_dotenv()

from cleverbot_final import CleverbotConversation

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.cleverbot = CleverbotConversation(max_context=100)





@bot.event
async def on_ready():
    print('Bot is ready.')
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(' \
                CREATE TABLE IF NOT EXISTS users \
                (id INTEGER PRIMARY KEY, \
                name TEXT) \
            ')

@bot.command()
async def adduser(ctx, member: discord.Member):
    print("adduser triggered")
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(' \
                INSERT INTO users (id, name) \
                VALUES (?, ?) \
            ', (member.id, member.name))
            await db.commit()
    await ctx.send(f'Added {member.name} to the database.')

@bot.command()
async def listusers(ctx):
    print("listusers triggered")
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(' \
                SELECT * FROM users \
            ')
            users = await cursor.fetchall()
    await ctx.send(f'Users: {users}')

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

