import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from colorama import Fore
from typing import Optional
from datetime import datetime
from pymongo import MongoClient
import motor.motor_asyncio as motor
import asyncio
load_dotenv()

"""
WIP:
- db stuff
- error handlers

"""

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all())
        self.extensions_dir = 'extensions'
        """
        The directory from which extensions are loaded.
        """
        self.excluded_extensions = [
        ]
        """
        Excluded extensions are excluded from the initial load. However, they can still be loaded manually latre.
        """
        self.important_extensions = [
            'cog_base',
            'helpers',
            'files'
        ]
        """
        Important extensions are extensions that are required for the bot to function properly. They cannot be unloaded.
        Currently the location of important extensions doesn't matter. In the future they might be kept track of by being in an `important` dir.
        """
        self.db_name = 'CatWithHorns'
        self.client = None
        self.db = None

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        await self.sync_all()

    async def setup_hook(self):
        await self.connect_motor()
        await self.setup_extensions()



    # extension functions

    async def _setup_extensions(self, directory: str):
        """
        Recursively loads all extensions in the given directory.
        """
        for file in os.listdir(f'./{directory}'):
            # print(f"In {directory} directory I see {file}")

            if file.endswith('.py') and file[:-3] not in self.excluded_extensions:
                name = file[:-3]
                ext = f"{directory.replace('/', '.')}.{name}"

                await self.load_extension(ext)
                print(f"{Fore.LIGHTYELLOW_EX}{name}{Fore.RESET} extension loaded")

            elif os.path.isdir(f'{directory}/{file}'):
                # print(f"Entering {file} directory")
                await self._setup_extensions(f"{directory}/{file}")
            else:
                # print(f"Skipping {file}")
                pass
    
    async def setup_extensions(self):
        """
        Loads all extensions in the extensions directory.
        """
        await self._setup_extensions(self.extensions_dir)

    def _find_extension(self, directory: str, ext: str) -> Optional[str]:
        """
        Recursively searches for an extension in the given directory.
        """
        for file in os.listdir(f'./{directory}'):
            
            if file.endswith('.py') and file[:-3] == ext:
                return f"{directory.replace('/', '.')}.{file[:-3]}"
            
            elif os.path.isdir(f'{directory}/{file}'):

                found_ext = self._find_extension(f"{directory}/{file}", ext)
                
                if found_ext is not None:
                    return found_ext
                
    def find_extension(self, ext: str) -> Optional[str]:
        """
        Searches for an extension in the extensions directory.
        """
        return self._find_extension(self.extensions_dir, ext)

    def ext_mechanism(self, func):
        """
        A decorator that wraps the extension management commands.
        """
        async def wrapper(ctx: commands.Context, ext: str):
            found_ext = bot.find_extension(ext)

            if found_ext is None:
                await ctx.send(f"Extension `{ext}` not found")
                return

            try:
                await func(ctx, found_ext)
            except Exception as e:
                await ctx.send(f"`{e}`")

        return wrapper

    def ext_report(self, author, action, ext):
        rn = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        print(f"{Fore.LIGHTBLACK_EX}[{rn}]{Fore.RESET} User {Fore.LIGHTMAGENTA_EX}{author}{Fore.RESET} {action} extension {Fore.LIGHTYELLOW_EX}{ext}{Fore.RESET}")



    # other setup functions

    async def sync_all(self) -> str:
        """
        Syncs all slash commands.

        Returns:
            A string containing the result of the sync.
        """
        print("Syncing command(s)")

        try:
            synced = await self.tree.sync()
            msg = f"Synced {len(synced)} command{'' if len(synced) == 1 else 's'}"
        except Exception as e:
            msg = f"`{e}`"

        print(msg)
        return msg

    async def connect_pymongo(self):
        try:
            self.client = MongoClient(os.getenv('MONGO_URI'))
            print("Connected to MongoDB (pymongo)")
            self.db = self.client.get_database(self.db_name)
            print(f"Connected to database {Fore.LIGHTMAGENTA_EX}{self.db.name}{Fore.RESET}")
        except Exception as e:
            print(e)

    async def close_pymongo(self):
        try:
            self.client.close()
            print("Closed MongoDB connection")
        except Exception as e:
            print(e)

    async def connect_motor(self):
        try:
            self.client = motor.AsyncIOMotorClient(os.getenv('MONGO_URI'))
            print("Connected to MongoDB (motor)")
            self.db = self.client.get_database(self.db_name)
            print(f"Connected to database {Fore.LIGHTMAGENTA_EX}{self.db.name}{Fore.RESET}")
        except Exception as e:
            print(e)

bot = MyBot()

@bot.command(name="load")
@bot.ext_mechanism
async def load(ctx: commands.Context, ext: str):
    await bot.load_extension(ext)
    await ctx.send(f"Loaded extension `{ext}`")
    bot.ext_report(ctx.author, "loaded", ext)

@bot.command(name="unload")
@bot.ext_mechanism
async def unload(ctx: commands.Context, ext: str):
    if ext in bot.important_extensions:
        await ctx.send(f"Extension `{ext}` is important and cannot be unloaded")
        return

    await bot.unload_extension(ext)
    await ctx.send(f"Unloaded extension `{ext}`")
    bot.ext_report(ctx.author, "unloaded", ext)

@bot.command(name="reload")
@bot.ext_mechanism
async def reload(ctx: commands.Context, ext: str):
    await bot.reload_extension(ext)
    await ctx.send(f"Reloaded extension `{ext}`")
    bot.ext_report(ctx.author, "reloaded", ext)

@bot.command()
async def sync(ctx):
    result = await bot.sync_all()
    await ctx.send(result)


bot.run(os.getenv('TOKEN'))