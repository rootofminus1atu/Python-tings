from typing import Optional
import discord
from discord.ext import commands
import calendar
import inflect
p = inflect.engine()

def pretty_date(date):
    return date.strftime(f"{p.ordinal(date.strftime('%d'))} %B %Y")

def pretty_day_month(day: int, month: int):
    return f"{p.ordinal(day)} of {calendar.month_name[month]}"

def ordinal(n):
    return f"{p.ordinal(n)}"
