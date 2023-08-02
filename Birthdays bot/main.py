import discord
from discord.ext import commands
from typing import Optional
from colorama import Fore
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all())
        self.excluded_cogs = [
            'purgatory',
            'help'
        ]
        self.client = None
        self.db = None

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    async def setup_hook(self):
        try:
            self.client = MongoClient(os.getenv('MONGO_URI'))
            print("Connected to MongoDB")
            self.db = self.client.get_database('CatWithHorns')
            print("Connected to database " + Fore.LIGHTMAGENTA_EX + "self.db.name" + Fore.RESET)
        except Exception as e:
            print(e)

        await self.load_cogs()

    async def load_cogs(self):
        for file in os.listdir('./cogs'):
            if file.endswith('.py') and file[:-3] not in self.excluded_cogs:
                print("Loading extension " + Fore.LIGHTYELLOW_EX + file[:-3] + Fore.RESET)
                await self.load_extension(f'cogs.{file[:-3]}')

    async def get_or_fetch_user(self, user_id: int) -> Optional[discord.User]:
        try:
            return self.get_user(user_id) or await self.fetch_user(user_id)
        except discord.NotFound:
            return None



bot = MyBot()

@bot.command()
async def load(ctx, cog):
    try:
        await bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Loaded cog `{cog}`")
    except Exception as e:
        await ctx.send(f"`{e}`")


@bot.command()
async def unload(ctx, cog):
    try:
        await bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"Unloaded cog `{cog}`")
    except Exception as e:
        await ctx.send(f"`{e}`")


@bot.command()
async def reload(ctx, cog):
    try:
        await bot.reload_extension(f"cogs.{cog}")
        await ctx.send(f"Reloaded cog `{cog}`")
    except Exception as e:
        await ctx.send(f"`{e}`")




@bot.command()
async def sync(ctx):
    print("Syncing command(s)")
    try: 
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        await ctx.send(f"Synced {len(synced)} command(s)")
    except Exception as e:
        await ctx.send(f"`{e}`")


bot.run(os.getenv('TOKEN'))
