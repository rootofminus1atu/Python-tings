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

    @commands.command(name="help2")
    async def help2(self, ctx):
        em = discord.Embed(
            title="Help",
            description="list of all commands",
            color=discord.Color.blurple())
        em.set_thumbnail(
            url=self.bot.user.avatar.url)

        command_dict = {}
        for command in self.bot.commands:
            if isinstance(command, app_commands.ApplicationCommand):
                if command.cog_name not in command_dict:
                    command_dict[command.cog_name] = []
                command_dict[command.cog_name].append(command)

        for cog_name, commands in command_dict.items():
            if cog_name:
                em.add_field(
                    name=cog_name,
                    value="\n".join([f"`/{c.name}` - {c.description}" for c in commands]),
                    inline=False
                )

        await ctx.send(embed=em)
    @app_commands.command(name="help3", description="help msg")
    async def help3(self, interaction: discord.Interaction):
        em = discord.Embed(
            title="Help",
            description="list of all commands",
            color=discord.Color.blurple())
        em.set_thumbnail(
            url=self.bot.user.avatar.url)

        for slash_command in self.bot.tree.walk_commands():
            em.add_field(
                name=slash_command.name,
                value=slash_command.description if slash_command.description else slash_command.name,
                inline=False)

        await interaction.response.send_message(embed=em)


async def setup(bot):
    await bot.add_cog(help(bot))
