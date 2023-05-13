import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
        
        
cached_messages = {}
cached_users = {}
        
@bot.event
async def on_raw_reaction_add(payload):
    return
    channel_id = payload.channel_id
    message_id = payload.message_id
    user_id = payload.user_id
    emoji = payload.emoji

    if message_id in cached_messages:
        message = cached_messages[message_id]
        channel = message.channel
    else:
        channel = await bot.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await channel.get_partial_message(message_id)
        cached_messages[message_id] = message

    if user_id in cached_users:
        user = cached_users[user_id]
    else:
        user = await bot.fetch_user(user_id)
        cached_users[user_id] = user

    # Print the reaction event
    print(f"User {user.name} reacted with {emoji} in channel {channel.name} to message {message.content}")
    await channel.send(f"User {user.name} reacted with {emoji} in channel {channel.name} to message {message.content}") 
    
    
prohibited_emojis = [
    '👽',
    '😈', 
    '<a:trishadance:886318268464365638>'
]

    
@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    message = reaction.message
    channel = message.channel
    color = discord.Color.blurple()
    
    if str(reaction.emoji) in prohibited_emojis:
        await reaction.clear()
        color = discord.Color.red()
    
    embed = discord.Embed( 
        description=f"Reacted with {reaction.emoji} in channel {channel.jump_url} to message {message.jump_url} ({message.content[:100]}{'...' if len(message.content) > 100 else ''})",
        color=color)
    embed.set_author(
        name=user.name, 
        icon_url=user.avatar.url)

    await channel.send(embed=embed)


@bot.tree.command(name="user", description="Get a user's info")
@app_commands.describe(user="which user lol")
async def user(interaction: discord.Interaction, user: discord.User):
    no_react_role = discord.utils.get(interaction.guild.roles, name="No reactions")

    if no_react_role is None:
        no_react_perms = interaction.guild.default_role.permissions
        no_react_perms.update(add_reactions=False)
        no_react_role = await interaction.guild.create_role(name="No reactions", permissions=no_react_perms)
    
    await user.add_roles(no_react_role)
    await interaction.response.send_message(f"{user} can't react anymore")


@bot.tree.command(name="ping")
@app_commands.checks.cooldown(1, 30)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")
    
@bot.command()
async def test(ctx):
    await ctx.send("test")
    
bot.run(os.getenv('BOT_KEY'))