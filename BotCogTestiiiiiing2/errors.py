import discord
from discord.ext import commands
from discord import app_commands


class TreeWithErrors(app_commands.CommandTree):
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print("on_tree_error called", interaction, error)
        if isinstance(error, CheckFailedLol):
            await interaction.response.send_message(str(error))
        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
        elif isinstance(error, NotInGuildError):
            await interaction.response.send_message(str(error))
        else:
            await interaction.response.send_message(f"Something went wrong... `{error}`")
            raise error


class CheckFailedLol(app_commands.CheckFailure):
    def __init__(self, lol_id: int, bot: commands.Bot):
        self.lol_id = lol_id
        self.bot = bot
        super().__init__(f"Failed to LOL (user) for {lol_id} ({bot.get_user(lol_id)!r})")


def lol_check(lol_id: int):
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id != lol_id:
            raise CheckFailedLol(lol_id, interaction.client)
        return True
    return app_commands.check(predicate)


class NotInGuildError(app_commands.CheckFailure):
    def __init__(self, guild_id: int, bot: commands.Bot):
        self.guild_id = guild_id
        self.bot = bot
        self.guild_name = self.bot.get_guild(guild_id)
        super().__init__(f"You must be in **{self.guild_name}** to execute that command")


def is_in_guild(guild_id: int):
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.guild_id != guild_id:
            raise NotInGuildError(guild_id, interaction.client)
        return True
    return app_commands.check(predicate)
