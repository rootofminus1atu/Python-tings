import io
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Select, View
from files import texts, goobers, lang_codes, quote_translation
import requests
import random
from datetime import datetime
import pytz
from PIL import Image, ImageDraw
import inflect
import os
from dotenv import load_dotenv
load_dotenv()
p = inflect.engine()


# more functionality, but it's still kinda messy


bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    papiez.start()


@tasks.loop(seconds=60)
async def papiez():
    channel = bot.get_channel(1034863959964143666)
    pl_date = datetime.now(pytz.timezone('Poland'))
    pl_time = pl_date.strftime('%H:%M')

    if pl_time == "21:37":
        await channel.send("papiez")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    lst = [1034863959964143666]  # bot-commands id
    if message.channel.id in lst:
        if message.embeds or message.attachments:
            await message.add_reaction('❤')
            return

        if message.content == 'cool':
            await message.channel.send("you too")
            return


@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")


@bot.tree.command(name="icecream", description="testing timeouts")
async def icecream(interaction: discord.Interaction):
    select = Select(
        placeholder="Choose a flavor",
        options=[
            discord.SelectOption(label="vanilla", emoji="🤍", description="yum"),
            discord.SelectOption(label="choco", emoji="🍫", description="yum"),
            discord.SelectOption(label="strawberry", emoji="🍓", description="yum")]
    )

    view = View(timeout=30)
    view.add_item(select)

    async def my_callback(interaction):
        await interaction.response.edit_message(content=f"Awesome, I like {select.values[0]} too!", view=view)

    select.callback = my_callback

    await interaction.response.send_message(view=view)


@bot.tree.command(name="embed", description="for testing embed designs")
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Quote:",
        description="wise words",
        color=0x000000)
    embed.set_author(
        name="John Paul the 2nd",
        icon_url="https://cdn.discordapp.com/emojis/934972840594264104.webp?size=96&quality=lossless")
    embed.add_field(
        name="Quote translation:",
        value=f"wise words(in english)",
        inline=True)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="popequote", description="pope John Paul the 2nd's wisdom")
async def pope_quote(interaction: discord.Interaction):

    quote = random.choice(list(quote_translation))

    embed = discord.Embed(
        title="Quote:",
        description=f"*{quote}*",
        color=0x000000)
    embed.set_author(
        name="John Paul the 2nd",
        icon_url="https://media.discordapp.net/attachments/1060711805028155453/1060713256576106606/sc2.png?width=390&height=390")
    embed.add_field(
        name="Quote translation:",
        value=f"*{quote_translation[quote]}*",
        inline=True)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="fox", description="get a random fox")
async def fox(interaction: discord.Interaction):
    foxer = requests.get("https://randomfox.ca/floof").json()
    await interaction.response.send_message(foxer["image"])


@bot.tree.command(name="what", description="what?")
async def what(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(texts))


@bot.tree.command(name="goober", description="Goofy Goobers Generator!")
async def goober(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(goobers))


@bot.tree.command(name="calculate", description="lol math")
@app_commands.describe(expression="Type help for help")
async def calc(interaction: discord.Interaction, expression: str):
    if expression.lower() == "help":
        await interaction.response.send_message(f"Here's your help message")  # could be an embed instead of a text msg
    else:
        try:
            await interaction.response.send_message(f"{expression} = {eval(expression)}")
        except:
            await interaction.response.send_message(f"that's too ugly")


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say="What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")


@bot.tree.command(name="translate", description="translate stuff lol")
@app_commands.describe(translate_from="translate from:", translate_to="translate to:", message="the message you want to translate:")
async def translate(interaction: discord.Interaction, translate_from: str, translate_to: str, message: str):
    first = translate_from.lower()
    second = translate_to.lower()

    if first not in lang_codes and second not in lang_codes:
        await interaction.response.send_message(f"Sorry, I don't recognize either of those as languages", ephemeral=True)
        return
    if first not in lang_codes:
        await interaction.response.send_message(f"Sorry, I don't recognize **{first}** as a language", ephemeral=True)
        return
    if second not in lang_codes:
        await interaction.response.send_message(f"Sorry, I don't recognize **{second}** as a language", ephemeral=True)
        return

    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/get"
    querystring = {
        "langpair": lang_codes[first] + "|" + lang_codes[second],
        "q": message,
        "mt": "1",
        "onlyprivate": "0",
        "de": "a@b.c"}
    headers = {
        "X-RapidAPI-Key": os.getenv('translation_key'),
        "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com"}
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    translated_msg = response['responseData']['translatedText']
    # print(response)  # for debugging
    # print(translated_msg)

    if response['quotaFinished'] is None:
        await interaction.response.send_message(f"One of those languages flew out of my head...", ephemeral=True)
        return

    embed = discord.Embed(
        color=0x000000)
    embed.set_author(
        name="Translation",
        icon_url="https://cdn.discordapp.com/emojis/934972840594264104.webp?size=96&quality=lossless")
    embed.add_field(
        name=f"From {first}:",
        value=message,
        inline=True)
    embed.add_field(
        name=f"To {second}:",
        value=translated_msg,
        inline=True)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="palette", description="Get a random color palette")
async def palette(interaction: discord.Interaction):
    # create an image with a black background
    wide = 300
    tall = int(wide/5)
    image = Image.new('RGB', (wide, tall), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # get 5 random colors
    url = "http://colormind.io/api/"
    data = {"model": "default"}

    response = requests.post(url, json=data).json()
    colors = response["result"]
    colors_better = [tuple(x) for x in colors]

    # draw rectangles with the random colors on the image
    x, y = 0, 0
    width, height = wide/5, tall
    for color in colors_better:
        draw.rectangle((x, y, x+width, y+height), fill=color)
        x += width

    # save the image to a file-like object
    image_data = io.BytesIO()
    image.save(image_data, 'PNG')
    image_data.seek(0)

    # send the image data as an attachment
    message = await bot.get_channel(1061811267834224649).send(file=discord.File(image_data, 'color_palette.png'))

    # get the url of the image from the message attachments
    image_url = message.attachments[0].url

    # send the image url in an embed
    embed = discord.Embed()
    embed.set_author(
        name="Here's your random color palette:",
        icon_url="https://media.discordapp.net/attachments/1060711805028155453/1061825040716402731/logo_beter.png")
    embed.set_image(
        url=image_url)
    embed.set_footer(
        text="Generated with colormind.io")

    # gg
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="serverinfo", description="Inforomation about the server!")
async def serverinfo(interaction: discord.Interaction):
    role_list = [str(role.name) for role in interaction.guild.roles if role.name != "@everyone"]
    co_owner_role = interaction.guild.get_role(1001472749711147040)
    creation_time = interaction.guild.created_at

    try:
        co_owners = ", ".join(str(member) for member in co_owner_role.members if member != interaction.guild.owner)
    except:
        co_owners = "Nobody!"

    embed = discord.Embed(
        title="Server information",
        description=f"""🔹**Name:** {interaction.guild.name}
        🔹**Id:** {interaction.guild.id}
        🔹**Owner:** {interaction.guild.owner}
        🔹**Co-owner(s):** {co_owners}""",
        color=0x397fbf)
    embed.add_field(
        name="Members:",
        value=f"""🔹**All:** {len(interaction.guild.members)}
        🔹**Online:** {sum(member.status!=discord.Status.offline for member in interaction.guild.members)}""",
        inline=True)
    embed.add_field(
        name="Channels:",
        value=f"""🔹**Text:** {len(interaction.guild.text_channels)}
        🔹**Voice:** {len(interaction.guild.voice_channels)}""",
        inline=True)
    embed.add_field(
        name=f"Roles ({len(role_list)}):",
        value=", ".join(role_list),
        inline=False)
    try:
        icon_url = interaction.guild.icon.url
        embed.set_thumbnail(url=icon_url)
    except:
        pass
    embed.set_footer(
        # ugliest datetime formating code ever
        text=f"""Server creation date: {creation_time.strftime(f'{p.ordinal(creation_time.strftime("%d"))} %B %Y')}""")

    await interaction.response.send_message(embed=embed)


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
        url=f"{bot.user.avatar.url}")
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


@bot.tree.command(name='choices')
@app_commands.describe(optionlol="pick a weather")
@app_commands.choices(optionlol=[
        app_commands.Choice(name="rainy", value="why do I need this"),
        app_commands.Choice(name="cloudy", value="why do I need this")
    ])
async def test(interaction: discord.Interaction, option: app_commands.Choice[str]):
    await interaction.response.send_message(f"You chose: {option.name}")


bot.run(os.getenv('bot_key'))
