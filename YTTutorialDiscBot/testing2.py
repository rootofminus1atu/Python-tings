import io
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View
import requests
from PIL import Image, ImageDraw
import inflect
import os
from dotenv import load_dotenv
load_dotenv()
p = inflect.engine()

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


# even more testing? why did I make so many files this is a mess


gibbal_id = 698905167629647882
luki_id = 531815121752686603
null_id = 611867495833403392


@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)



@bot.tree.command(name="button", description="click me")
async def button(interaction: discord.Interaction):

    button = discord.ui.Button(label="Click me!", style=discord.ButtonStyle.gray)

    async def button_callback(interaction):
        await interaction.response.edit_message(content="You clicked me")

    button.callback = button_callback

    view = View()
    view.add_item(button)

    await interaction.response.send_message("hi", view=view)


@bot.tree.command(name="botinfo", description="Info about the bot")
async def botinfo(interaction: discord.Interaction):
    creation_time = bot.user.created_at
    bot_info = await bot.application_info()
    owner = bot_info.owner

    embed = discord.Embed(
        title=f"{bot.user}",
        description=f"{bot.user.name} knows much, tells some. {bot.user.name} knows many things others do not. {bot.user.name} wishes you well.",
        color=0x397fbf)
    embed.set_thumbnail(
        url=bot.user.avatar.url)
    embed.add_field(
        name="Dev:",
        value=f"{owner.name}#{owner.discriminator}",
        inline=True)
    embed.add_field(
        name="Library:",
        value=f"discord.py version {discord.__version__}",
        inline=True)
    embed.set_footer(
        text=f"""Creation date: {creation_time.strftime(f'{p.ordinal(creation_time.strftime("%d"))} %B %Y')}""")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="palette", description="Generates a random color palette")
async def palette(interaction: discord.Interaction):
    async def get_color_palette():
        try:
            response = requests.post("http://colormind.io/api/", json={"model": "default"}).json()
            colors = response["result"]
            colors = [tuple(x) for x in colors]
        except requests.exceptions.RequestException as e:
            return None, f"An error occurred while getting the color palette: {e}"

        return colors, None

    async def create_image(colors):
        # create an image with a black background
        wide = 300
        tall = int(wide / 5)
        image = Image.new("RGB", (wide, tall), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        # draw squares with those colors
        x, y = 0, 0
        width, height = wide / 5, tall
        for color in colors:
            draw.rectangle((x, y, x + width, y + height), fill=color)
            x += width

        # save the image
        image_data = io.BytesIO()
        image.save(image_data, "PNG")
        image_data.seek(0)
        return image_data

    colors, error = await get_color_palette()

    if error:
        return await interaction.response.send_message(embed=discord.Embed(description=error))

    image = await create_image(colors)
    file = discord.File(image, "color_palette.png")
    embed = discord.Embed()
    embed.set_author(
        name="Here's your random color palette:",
        icon_url="https://media.discordapp.net/attachments/1060711805028155453/1061825040716402731/logo_beter.png")
    embed.set_image(
        url="attachment://color_palette.png")
    embed.set_footer(
        text="Generated with colormind.io")

    button = discord.ui.Button(label="Generate again", style=discord.ButtonStyle.gray)
    view = View()
    view.add_item(button)

    async def button_callback(interaction):
        colors, error = await get_color_palette()

        if error:
            return await interaction.response.send_message(embed=discord.Embed(description=error))

        image = await create_image(colors)
        file = discord.File(image, "color_palette.png")
        embed = discord.Embed()
        embed.set_author(
            name="Here's your random color palette:",
            icon_url="https://media.discordapp.net/attachments/1060711805028155453/1061825040716402731/logo_beter.png")
        embed.set_image(
            url="attachment://color_palette.png")
        embed.set_footer(
            text="Generated with colormind.io")

        await interaction.response.edit_message(embed=embed, view=view, attachments=[file])

    button.callback = button_callback

    await interaction.response.send_message(file=file, embed=embed, view=view)


@bot.tree.command(name="greet", description="Who should I greet?")
@app_commands.describe(user="Who do you want to greet?")
async def greet(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"Hello {user.mention}")


# hmmmm maybe I could create a class of languages
# and use an arg like this:
# language: Languages
# maybe who knows
@bot.tree.command(name="say", description="HELLO")
@app_commands.describe(text="What I'll say:", channel="Where I'll say it:")
async def say(interaction: discord.Interaction, text: str, channel: discord.TextChannel):
    await channel.send(text)
    await interaction.response.send_message("The message was sent", ephemeral=True)






bot.run(os.getenv('bot_key'))
