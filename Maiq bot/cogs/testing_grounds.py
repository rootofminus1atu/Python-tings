import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore


class testing_grounds(commands.GroupCog, name="uwu"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")


    @app_commands.command(name="ping", description="...")
    async def _ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("pong!")
    
    @app_commands.command(name="command", description="...")
    async def _cmd(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("uwu")


async def setup(bot):
    await bot.add_cog(testing_grounds(bot))
