import discord
from discord.ext import commands
from discord import app_commands
from colorama import Back, Fore, Style


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @app_commands.command()
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Greetings.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def admin(self, ctx):
        await ctx.send("You seem like an admin.")


async def setup(bot):
    await bot.add_cog(ping(bot))
