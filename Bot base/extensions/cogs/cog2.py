import discord
from discord.ext import commands
from discord import app_commands

from extensions.cog_base import CogBase

class cog2(CogBase):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("hello")

async def setup(bot):
    await bot.add_cog(cog2(bot))