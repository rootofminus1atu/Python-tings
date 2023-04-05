import discord
from discord.ext import commands
from discord import app_commands


class TreeWithErrors(app_commands.CommandTree):
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print("on_tree_error called", interaction, error)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(str(error), ephemeral=True)
        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!", ephemeral=True)
        elif isinstance(error, NotInGuildError):
            await interaction.response.send_message(str(error), ephemeral=True)
        else:
            await interaction.response.send_message(f"Something went wrong... `{error}`")
            raise error

"""def is_mod(interaction: discord.Interaction):
    return interaction.user.guild_permissions.manage_guild is True
def is_owner():
    def predicate(interaction: discord.Interaction):
        if interaction.user == interaction.guild.owner:
            return True
    return app_commands.check(predicate)"""


def has_mod_or_roles(special_roles):
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.guild_permissions.moderate_members:
            return True

        user_roles = [role.id for role in interaction.user.roles]

        for name, role_id in special_roles:
            # print(name, role_id, user_roles, special_roles)
            if role_id in user_roles:
                return True

        raise app_commands.MissingPermissions(['moderate_members'])
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