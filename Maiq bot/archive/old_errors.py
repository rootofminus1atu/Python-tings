"""import discord
from discord.ext import commands
from discord import app_commands, Interaction
from colorama import Back, Fore, Style


class NotInGuildError(app_commands.CheckFailure):
    def __init__(self, guild_id, bot: commands.Bot):
        self.guild_id = guild_id
        self.bot = bot
        super().__init__(
            f"You must be in the server '{bot.get_guild(guild_id)!r}' with ID {guild_id} to use this command.")


class errors(commands.Cog):


    @staticmethod
    def is_in_guild(guild_id):
        async def predicate(interaction: Interaction[commands.Bot]):
            if interaction.guild and interaction.guild.id == guild_id:
                return True
            else:
                raise NotInGuildError(guild_id, interaction.client)
        return app_commands.check(predicate)


    @staticmethod
    async def on_tree_error(interaction: Interaction[commands.Bot], error: Exception):
        print("on_tree_error called", interaction, error)
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(f"You're missing permissions to use that")
        elif isinstance(error, NotInGuildError):
            print("on tree error was used")
            await interaction.response.send_message(str(error))
        else:
            print("ELSE WAS REACHED")
            raise error


async def setup(bot):
    bot.tree.on_error = errors.on_tree_error
    await bot.add_cog(errors())"""

from email import errors
from discord.ext import commands
from discord import app_commands, Interaction


class CheckFailedLol(app_commands.CheckFailure):
    def __init__(self, lol_id: int, bot: commands.Bot):
        self.lol_id = lol_id
        self.bot = bot
        super().__init__(f"Failed to LOL (user) for {lol_id} ({bot.get_user(lol_id)!r})")


class NotInGuildError(app_commands.CheckFailure):
    def __init__(self, guild_id: int, bot: commands.Bot):
        self.guild_id = guild_id
        self.bot = bot
        super().__init__(
            f"You must be in the server '{bot.get_guild(guild_id)!r}' with ID {guild_id} to use this command.")

class errors(commands.Cog):
    @staticmethod
    def lol_check(lol_id: int):
        async def actual(interaction: Interaction[commands.Bot]) -> bool:
            if interaction.user.id != lol_id:
                raise CheckFailedLol(lol_id, interaction.client)
            return True
        return app_commands.check(actual)

    @staticmethod
    def is_in_guild(guild_id):
        async def predicate(interaction: Interaction[commands.Bot]):
            if interaction.guild and interaction.guild.id == guild_id:
                return True
            else:
                raise NotInGuildError(guild_id, interaction.client)

        return app_commands.check(predicate)

    @staticmethod
    async def on_tree_error(interaction: Interaction[commands.Bot], error: Exception):
        print("on_tree_error called", interaction, error)
        if isinstance(error, CheckFailedLol):
            await interaction.response.send_message(str(error))
        if isinstance(error, NotInGuildError):
            await interaction.response.send_message(str(error))
        else:
            raise error


class Test(commands.Cog):
    @app_commands.command()
    @errors.lol_check(150665783268212746)
    async def test2(self, interaction: Interaction[commands.Bot]):
        await interaction.response.send_message("Test")

    """@app_commands.command(name="test", description="are u mod")
    @errors.is_in_guild(1031977836849922108)
    # @app_commands.check(is_mod)
    async def test(self, interaction: Interaction[commands.Bot]):
        await interaction.response.send_message("you are a mod!")"""


async def setup(bot: commands.Bot):
    await bot.add_cog(errors())
    bot.tree.on_error = errors.on_tree_error
    await bot.add_cog(Test())