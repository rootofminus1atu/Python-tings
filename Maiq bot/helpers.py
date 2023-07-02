from typing import Optional
import discord
import inflect
p = inflect.engine()

def pretty_date(date):
    return date.strftime(f"{p.ordinal(date.strftime('%d'))} %B %Y")

async def get_user_from_id(bot, user_id) -> Optional[discord.User]:
    try:
        return bot.get_user(user_id) or await bot.fetch_user(user_id)
    except discord.NotFound:
        return None