from typing import Optional
import discord
import calendar
import inflect
p = inflect.engine()

def pretty_date(date):
    return date.strftime(f"{p.ordinal(date.strftime('%d'))} %B %Y")

def pretty_day_month(day: int, month: int):
    return f"{p.ordinal(day)} of {calendar.month_name[month]}"

async def get_or_fetch_user(bot, user_id) -> Optional[discord.User]:
    try:
        return bot.get_user(user_id) or await bot.fetch_user(user_id)
    except discord.NotFound:
        return None
    
print(pretty_day_month(3, 6))