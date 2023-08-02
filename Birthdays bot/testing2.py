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


class BirthdaysManager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.collection = self.bot.db['serious_birthdays_config']

    def create_config(self, situation, and_birthday=None, time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        place, channel = situation

        # if channel == if we're in a server
        if channel:
            chunk = {
                "server_id": place.id,
                "server_name": place.name,
                "channel_id": channel.id,
                "channel_name": channel.name
            }
        else:
            chunk = {
                "user_id": place.id,
                "user_name": place.name
            }
        
        chunk.update({
            "time": time,
            "timezone": timezone,
            "birthdays": []
        })

        if and_birthday:
            chunk["birthdays"].append(and_birthday)

        print("Created config:", chunk)
        self.collection.insert_one(chunk)

    def get_config(self, situation):
        place, channel = situation

        if not channel:
            return self.collection.find_one({"user_id": place.id})
        else:
            return self.collection.find_one({"server_id": place.id})

    def add_birthday(self, space, birthday):
        place, channel = space

        if not channel:
            self.collection.update_one({"user_id": place.id}, {"$push": {"birthdays": birthday}})
        else:
            self.collection.update_one({"server_id": place.id}, {"$push": {"birthdays": birthday}})

    def get_person_birthday(self, space, person):
        place, channel = space

        if not channel:
            return self.collection.find_one({"server_id": place.id, "birthdays": {"$elemMatch": {"person": person}}})
        else:
            return self.collection.find_one({"user_id": place.id, "birthdays": {"$elemMatch": {"person": person}}})
    

manager = BirthdaysManager(MyBot("test"))

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
        situation = (server, channel)
    else:
        situation = (user, None)

    if not manager.get_config(situation):
        manager.create_config(situation, and_birthday=birthday)
        print(f"Added {person}'s birthday on {day}/{month}.")
    else:
        if manager.get_person_birthday(situation, person):
            print(f"{person}'s birthday already exists.")
        else:
            manager.add_birthday(situation, birthday)
            print(f"Added {person}'s birthday on {day}/{month}.")
