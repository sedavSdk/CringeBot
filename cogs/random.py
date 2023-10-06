from discord.ext import commands
import discord
from discord import app_commands
from random import randint

class CogPlay(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="coin", description="Кидает монетку")
    async def coinFlip(self, interaction: discord.Interaction):
        r = randint(0, 1)
        if r == 0:
            await interaction.response.send_message(content="Решка")
        else:
            await interaction.response.send_message(content="Орел")
    
    @app_commands.command(name="random", description="Случайное число от 1 до введенного")
    async def random(self, interaction: discord.Interaction, n : int):
        r = randint(0, n)
        await interaction.response.send_message(content=f"Случайное число от 1 до {n}: `{r}`")
