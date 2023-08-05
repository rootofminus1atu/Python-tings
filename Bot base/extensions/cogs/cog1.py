import discord
from discord.ext import commands
from discord import app_commands

from extensions.cog_base import CogBase

class cog1(CogBase):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def find(self, ctx, name: str):
        ext = self.bot.find_extension(name)
        await ctx.send(f"Result: {ext} (ok)")

async def setup(bot):
    await bot.add_cog(cog1(bot))