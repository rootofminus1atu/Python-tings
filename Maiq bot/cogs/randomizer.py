import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View
from colorama import Back, Fore, Style
import requests
from PIL import Image, ImageDraw
import io


class randomizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="fox", description="Mai'q will look for fluffy creatures")
    async def fox(self, interaction: discord.Interaction):
        fox = requests.get("https://randomfox.ca/floof").json()

        embed = discord.Embed(
            title="🦊 Mai'q found a fox",
            color=0xf77c1e)
        embed.set_image(
            url=fox["image"])

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dog", description="Mai'q will look for fluffy creatures")
    async def dog(self, interaction: discord.Interaction):
        dog = requests.get("https://dog.ceo/api/breeds/image/random").json()

        embed = discord.Embed(
            title="🐶 Mai'q found a dog",
            color=0x8f5a28)
        embed.set_image(
            url=dog["message"])

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cat", description="Mai'q will look for fluffy creatures")
    async def cat(self, interaction: discord.Interaction):
        cat = requests.get("https://aws.random.cat/meow").json()

        embed = discord.Embed(
            title="🐱 Mai'q found a Khajiit",
            color=0xcc9923)
        embed.set_image(
            url=cat["file"])

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="palette", description="Painting a nice-looking color palette is easy for Mai'q")
    async def palette(self, interaction: discord.Interaction):
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

        def rgb_to_hex(tup):
            r, g, b = tup
            return '0x{:02x}{:02x}{:02x}'.format(r, g, b)

        colors, error = await get_color_palette()

        if error:
            return await interaction.response.send_message(embed=discord.Embed(description=error))

        image = await create_image(colors)
        file = discord.File(image, "color_palette.png")
        embed = discord.Embed(
            color=discord.Color.from_rgb(*colors[0]))
        embed.set_author(
            name="Mai'q painted this:",
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
            embed = discord.Embed(
                color=discord.Color.from_rgb(*colors[0]))
            embed.set_author(
                name="Mai'q Painted this:",
                icon_url="https://media.discordapp.net/attachments/1060711805028155453/1061825040716402731/logo_beter.png")
            embed.set_image(
                url="attachment://color_palette.png")
            embed.set_footer(
                text="Generated with colormind.io")

            await interaction.response.edit_message(attachments=[file], embed=embed, view=view)

        button.callback = button_callback

        await interaction.response.send_message(file=file, embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(randomizer(bot))
