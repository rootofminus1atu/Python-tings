import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
load_dotenv()
from errors import *
from db.db_manager import DbManager

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            tree_cls=TreeWithErrors)
        self.excluded_cogs = [
            'purgatory'
        ]
        self.db_manager = None

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    async def setup_hook(self):
        await self.load_cogs()
        self.db_manager = DbManager()

    async def load_cogs(self):
        for file in os.listdir('./cogs'):
            if file.endswith('.py') and file[:-3] not in self.excluded_cogs:
                await self.load_extension(f'cogs.{file[:-3]}')


bot = MyBot()


@bot.command()
async def load(ctx, cog):
    try:
        if ctx.author.guild_permissions.administrator:
            await bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Loaded cog `{cog}`")
        else:
            await ctx.send("Mai'q will not listen to you.")
    except Exception as e:
        await ctx.send(f"`{e}`")


@bot.command()
async def unload(ctx, cog):
    try:
        if ctx.author.guild_permissions.administrator:
            await bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"Unloaded cog `{cog}`")
        else:
            await ctx.send("Mai'q will not listen to you.")
    except Exception as e:
        await ctx.send(f"`{e}`")


@bot.command()
async def reload(ctx, cog):
    try:
        if ctx.author.guild_permissions.administrator:
            await bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Reloaded cog `{cog}`")
        else:
            await ctx.send("Mai'q will not listen to you.")
    except Exception as e:
        await ctx.send(f"`{e}`")



@bot.tree.command(name="ping")
@app_commands.checks.cooldown(1, 30)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

"""
class NotInGuildError(app_commands.CheckFailure):
    def __init__(self, guild_id: int, bot: commands.Bot):
        self.guild_id = guild_id
        self.bot = bot
        super().__init__(
            f"You must be in the server '{bot.get_guild(guild_id)!r}' with ID {guild_id} to use this command.")

async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        return await interaction.response.send_message(f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
    elif isinstance(error, app_commands.MissingPermissions):
        return await interaction.response.send_message(f"You're missing permissions to use that")
    elif isinstance(error, NotInGuildError):
        return await interaction.response.send_message(str(error))
    else:
        raise error
bot.tree.on_error = on_tree_error"""


# asyncio.run(load_cogs())
bot.run(os.getenv('bot_key'))
