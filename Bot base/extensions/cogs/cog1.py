import discord
from discord.ext import commands
from discord import app_commands
from typing import List, Literal, Tuple, Dict

from extensions.important.cog_base import CogBase

class cog1(CogBase, name="Testing grounds"):
    """
    This cog is cog1 lol
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="find", description="Let's see if an extension named that exists lol")
    async def find(self, ctx: commands.Context, name: str):
        ext = self.bot.find_extension(name)
        await ctx.send(f"Result: {ext} (ok)")

    @app_commands.command(name="hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello!")

    @commands.command()
    async def test(self, ctx: commands.Context):
        cogsss: List[commands.Cog] = self.bot.cogs
        print(cogsss)
        
        embeds = []

        for i, (name, cog) in enumerate(cogsss.items()):
            print("=====================================")
            found_coms: List[commands.Command] = cog.get_commands()
            found_slashs: List[app_commands.Command] = cog.get_app_commands()
            print(found_coms, found_slashs)

            
            embed = discord.Embed(
                title=f"{i+1}. {name}",
                description=cog.description if cog.description else "No description provided",
                color=discord.Color.random())

            for com in found_coms:
                params = [f"{param.name}: {param.annotation}" for param in com.clean_params.values()]
                params_str = ", ".join([f"[{param.name}]" for param in com.clean_params.values()])
                print(f"Command: {com.name}\nDescription: {com.description}\nParams: {params}")

                embed.add_field(
                    name=f"Command: {com.name} {params_str}",
                    value=com.description if com.description else "No description provided",
                    inline=False
                )

            for slash in found_slashs:
                params = [f"{param.name}" for param in slash.parameters]

                params_str = " ".join([f"[{param.name}]" for param in slash.parameters])

                embed.add_field(
                    name=f"App command: {slash.name} {params_str}",
                    value=slash.description if slash.description else "No description provided",
                    inline=False
                )

            embeds.append(embed)
            
        await ctx.send(embeds=embeds)

    @app_commands.command(name="choice", description="testing autocompletion")
    async def choice(self, interaction: discord.Interaction, item: str):
        """
        I wonder will this long description be seen?
        """
        await interaction.response.send_message(f"Your choice: {item}")

    @choice.autocomplete(name="item")
    async def choice_autocompletion(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        options = [
            "Mojito",
            "Cosmopolitan",
            "Old Fashioned",
            "Piña Colada",
            "Martini",
            "Margarita",
            "Moscow Mule",
            "Sangria",
            "Mai Tai",
            "Long Island Iced Tea",
            "Whiskey Sour",
            "Bloody Mary",
            "Negroni",
            "White Russian",
            "Bellini",
            "Caipirinha",
            "Pisco Sour",
            "Gin and Tonic",
            "Tequila Sunrise",
            "Daiquiri",
            "Paloma",
            "Irish Coffee",
            "Zombie",
            "Singapore Sling",
            "Blue Lagoon",
            "Sex on the Beach",
            "Black Russian",
            "Tom Collins",
            "Pina Colada",
            "Amaretto Sour",
            "Bahama Mama",
            "Blue Hawaii",
            "Alabama Slammer",
            "Sea Breeze",
            "Black Velvet",
            "Boulevardier",
            "Bronx",
            "Bee's Knees",
            "Champagne Cocktail",
            "Clover Club",
            "Cuba Libre",
            "Dark 'n' Stormy",
            "Espresso Martini",
            "French 75",
            "French Connection",
            "Gimlet",
            "Godfather",
            "Harvey Wallbanger",
            "Hemingway Daiquiri",
            "Horse's Neck",
            "Hurricane",
            "Jack Rose",
            "Kamikaze",
            "Kir",
            "Lemon Drop Martini",
            "Lynchburg Lemonade",
            "Mai Tai",
            "Manhattan",
            "Martinez",
            "Midori Sour",
            "Mimosa",
            "Mint Julep",
            "Mudslide",
            "New York Sour",
            "Painkiller",
            "Paradise",
            "Planters Punch",
            "Porto Flip",
            "Red Snapper",
            "Rob Roy",
            "Rusty Nail",
            "Sazerac",
            "Sidecar",
            "Stinger",
            "Tequila Sunrise",
            "Vesper",
            "Whiskey Sour",
            "White Lady",
            "Yellow Bird",
            "Zombie"
        ]

        choices = [app_commands.Choice(name=drink_choice, value=drink_choice) for drink_choice in options if current.lower() in drink_choice.lower()]
        
        return choices[:25]
    
async def setup(bot):
    await bot.add_cog(cog1(bot))