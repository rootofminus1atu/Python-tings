import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from colorama import Fore
from typing import Optional
from datetime import datetime
import asyncio
load_dotenv()


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all())
        self.extensions_dir = 'extensions'
        self.excluded_extensions = [
        ]
        self.important_extensions = [
            'cog_base',
            'helpers',
            'files'
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
        """
        try:
            self.client = MongoClient(os.getenv('MONGO_URI'))
            print("Connected to MongoDB")
            self.db = self.client.get_database('CatWithHorns')
            print("Connected to database " + Fore.LIGHTMAGENTA_EX + "self.db.name" + Fore.RESET)
        except Exception as e:
            print(e)
        """
        await self.setup_extensions()

    def replace_slashes_with_dots(self, input_string):
        return input_string.replace('/', '.')

    async def _setup_extensions(self, directory: str):
        for file in os.listdir(f'./{directory}'):
            # print(f"In {directory} directory I see {file}")

            if file.endswith('.py') and file[:-3] not in self.excluded_extensions:
                name = file[:-3]
                ext = f'{self.replace_slashes_with_dots(directory)}.{name}'
                print(f"{Fore.LIGHTYELLOW_EX}{name}{Fore.RESET} extension found, loading...")
                await self.load_extension(ext)
            elif os.path.isdir(f'{directory}/{file}'):
                # print(f"Entering {file} directory")
                await self._setup_extensions(f"{directory}/{file}")
            else:
                # print(f"Skipping {file}")
                pass
    
    async def setup_extensions(self):
        await self._setup_extensions(self.extensions_dir)

    def _find_extension(self, directory: str, name: str) -> Optional[str]:
        for file in os.listdir(f'./{directory}'):
            if file.endswith('.py') and file[:-3] == name:
                return f'{self.replace_slashes_with_dots(directory)}.{file[:-3]}'
            elif os.path.isdir(f'{directory}/{file}'):
                ext = self._find_extension(f"{directory}/{file}", name)
                if ext is not None:
                    return ext
                
    def find_extension(self, name: str) -> Optional[str]:
        return self._find_extension(self.extensions_dir, name)

    def ext_mechanism(self, func):
        async def wrapper(ctx, ext):
            found_ext = bot.find_extension(ext)

            if found_ext is None:
                await ctx.send(f"Extension `{ext}` not found")
                return

            try:
                await func(ctx, ext)
            except Exception as e:
                await ctx.send(f"`{e}`")
        return wrapper

    def ext_report(self, author, action, ext):
        rn = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        print(f"{Fore.LIGHTBLACK_EX}[{rn}]{Fore.RESET} User {Fore.LIGHTMAGENTA_EX}{author}{Fore.RESET} {action} extension {Fore.LIGHTYELLOW_EX}{ext}{Fore.RESET}")

    async def get_or_fetch_user(self, user_id: int) -> Optional[discord.User]:
        try:
            return self.get_user(user_id) or await self.fetch_user(user_id)
        except discord.NotFound:
            return None

bot = MyBot()

@bot.command(name="load")
@bot.ext_mechanism
async def load(ctx, ext):
    await bot.load_extension(f"extensions.{ext}")
    await ctx.send(f"Loaded extension `{ext}`")
    bot.ext_report(ctx.author, "loaded", ext)

@bot.command(name="unload")
@bot.ext_mechanism
async def unload(ctx, ext):
    if ext in bot.important_extensions:
        await ctx.send(f"Extension `{ext}` is important and cannot be unloaded")
        return

    await bot.unload_extension(f"extensions.{ext}")
    await ctx.send(f"Unloaded extension `{ext}`")
    bot.ext_report(ctx.author, "unloaded", ext)

@bot.command(name="reload")
@bot.ext_mechanism
async def reload(ctx, ext):
    await bot.reload_extension(f"extensions.{ext}")
    await ctx.send(f"Reloaded extension `{ext}`")
    bot.ext_report(ctx.author, "reloaded", ext)



@bot.command()
async def sync(ctx):
    print("Syncing command(s)")
    try: 
        synced = await bot.tree.sync()
        msg = f"Synced {len(synced)} command{'' if len(synced) == 1 else 's'}"
        print(msg)
        await ctx.send(msg)
    except Exception as e:
        await ctx.send(f"`{e}`")


bot.run(os.getenv('TOKEN'))