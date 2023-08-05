import discord
from discord.ext import commands
from discord import app_commands
from typing import List

from extensions.important.cog_base import CogBase

class cog1(CogBase):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="find", description="Let's see if an extension named that exists lol")
    async def find(self, ctx: commands.Context, name: str):
        ext = self.bot.find_extension(name)
        await ctx.send(f"Result: {ext} (ok)")

    @app_commands.command(name="hello", description="Sends a hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("hello")

    @commands.command()
    async def test(self, ctx: commands.Context):
        cogsss: List[commands.Cog] = self.bot.cogs
        print(cogsss)
        
        for name, cog in cogsss.items():
            print("=====================================")
            found_coms: List[commands.Command] = cog.get_commands()
            found_slashs: List[commands.app_command] = cog.get_app_commands()
            print(found_coms, found_slashs)

            for com in found_coms:
                params = [f"{param.name}: {param.annotation}" for param in com.clean_params.values()]
                print(f"Command: {com.name}\nDescription: {com.description}\nParams: {params}")

        await ctx.send(f"{cogsss}")

async def setup(bot):
    await bot.add_cog(cog1(bot))