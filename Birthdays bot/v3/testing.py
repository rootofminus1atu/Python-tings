import discord
from discord.ext import commands
from typing import Optional, Tuple
import timeit

DEFAULT_TIME = 8
DEFAULT_TIMEZONE = "UTC"

class MyGuild(discord.Guild):
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MyUser():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MyBot(commands.Bot):
    def __init__(self, name):
        self.name = name

class MyInteraction():
    def __init__(self, guild, channel, user):
        self.guild = guild
        self.channel = channel
        self.user = user

class MyChannel(discord.TextChannel):
    def __init__(self, id, name):
        self.id = id
        self.name = name



class BirthdayManager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # self.collection = self.bot.db['serious_birthdays_config']

    def create_config(self, space, time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        raise NotImplementedError

    def get_config(self, space):
        raise NotImplementedError

    def add_birthday(self, space, birthday):
        raise NotImplementedError

    def get_person_birthday(self, space, person):
        raise NotImplementedError

class ServerManager(BirthdayManager):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    def create_config(self, space: Tuple[discord.Guild, discord.TextChannel], time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        server, channel = space
        chunk = {
            "server_id": server.id,
            "server_name": server.name,
            "channel_id": channel.id,
            "channel_name": channel.name,
            "time": time,
            "timezone": timezone,
            "birthdays": []
        }
        print("Inserting", chunk)

    def get_config(self, space: Tuple[discord.Guild, discord.TextChannel]) -> Optional[dict]:
        server, _ = space
        print("Getting config for", server)

    def add_birthday(self, space: Tuple[discord.Guild, discord.TextChannel], birthday):
        server, _ = space
        print("Adding birthday", birthday, "to", server)

    def get_person_birthday(self, space: Tuple[discord.Guild, discord.TextChannel], person):
        server, _ = space
        print("Getting birthday for", person, "in", server)

class DmManager(BirthdayManager):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    def create_config(self, space: Tuple[discord.User], time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        user = space[0]
        chunk = {
            "user_id": user.id,
            "user_name": user.name,
            "time": time,
            "timezone": timezone,
            "birthdays": []
        }
        print("Inserting", chunk)

    def get_config(self, space: Tuple[discord.User]) -> Optional[dict]:
        user = space[0]
        print("Getting config for", user)

    def add_birthday(self, space: Tuple[discord.User], birthday):
        user, = space
        print("Adding birthday", birthday, "to", user)

    def get_person_birthday(self, space: Tuple[discord.User], person):
        user = space[0]
        print("Getting birthday for", person, "in", user)

"""
Mock example of bot commands using this new design pattern can be seen below
"""

def mock_command_add_birthday_server(bot, interaction, person, day, month):
    if not person or not day or not month:
        print("lol failed 1st check")
        return
    
    birthday = {
        "person": person,
        "day": day,
        "month": month
    }

    # either server
    server = interaction.guild
    channel = interaction.channel
    # or dm
    user = interaction.user

    if server:
        manager = ServerManager(bot)
        situation = (server, channel)
    else:
        manager = DmManager(bot)
        situation = (user,)

    if not manager.get_config(situation):
        manager.create_config(situation)
        print(f"Added {person}'s birthday on {day}/{month}.")
    else:
        if manager.get_person_birthday(situation, person):
            print(f"{person}'s birthday already exists.")
        else:
            manager.add_birthday(situation, birthday)
            print(f"Added {person}'s birthday on {day}/{month}.")

lol_bot = MyBot("lol")

# works fine
server_interaction = MyInteraction(MyGuild(999, "server"), MyChannel(999, "channel"), MyUser(5, "invoker"))
mock_command_add_birthday_server(lol_bot, server_interaction, "someone else", 12, 3)

# doesn't work fine
# the time becomes None
dm_interaction = MyInteraction(None, None, MyUser(999, "someone"))
mock_command_add_birthday_server(lol_bot, dm_interaction, "someone", 1, 4)
