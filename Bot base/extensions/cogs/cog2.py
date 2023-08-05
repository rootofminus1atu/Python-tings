import discord
from discord.ext import commands
from discord import app_commands

from extensions.important.cog_base import CogBase

class cog2(CogBase):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="users")
    async def users(self, ctx):
        users = await self.bot.user_manager.get_all_users()
        print(users)
        await ctx.send(f"Users: {', '.join([user['first_name'] for user in users])}")

async def setup(bot):
    await bot.add_cog(cog2(bot))