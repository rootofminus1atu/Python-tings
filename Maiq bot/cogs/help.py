import discord
from discord.ext import commands
from discord import app_commands
from colorama import Back, Fore, Style

# to-do
# make a working help command (hard)


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="help", description="help msg")
    async def help(self, interaction: discord.Interaction):
        em = discord.Embed(
            title="Help",
            description="Mai'q knows many commands.",
            color=discord.Color.blurple())
        em.set_thumbnail(
            url=self.bot.user.avatar.url)

        cmdstr = ""
        for cogname, cog in self.bot.cogs.items():
            cogcmds = cog.walk_commands()
            for command in cogcmds:
                cmdstr += f"{command.name}\n"
            em.add_field(
                name=cogname,
                value=cmdstr,
                inline=False)
            cmdstr = ""

        await interaction.response.send_message(embed=em)

    @app_commands.command(name="help2", description="help msg")
    async def help2(self, interaction: discord.Interaction):
        em = discord.Embed(
            title="Help",
            description="list of all commands",
            color=discord.Color.blurple())
        em.set_thumbnail(
            url=self.bot.user.avatar.url)

        for slash_command in self.bot.tree.walk_commands():
            em.add_field(name=slash_command.name,
                         value=slash_command.description if slash_command.description else slash_command.name,
                         inline=False)
            # fallbacks to the command name incase command description is not defined

        await interaction.response.send_message(embed=em)


async def setup(bot):
    await bot.add_cog(help(bot))
