import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Modal
from discord.components import TextInput
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

"""def is_in_guild(guild_id):
    async def predicate(ctx):
        print(ctx.guild)
        print(ctx.guild.id)
        print(guild_id)
        print(ctx.guild and ctx.guild.id == guild_id)
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)"""



"""class NotInGuildError(app_commands.CheckFailure):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        super().__init__(f"You must be in guild with id {guild_id} to use this command.")

def is_in_guild(guild_id):
    async def predicate(interaction: discord.Interaction):
        if interaction.guild and interaction.guild.id == guild_id:
            return True
        else:
            raise NotInGuildError(guild_id)
    return app_commands.check(predicate)"""

