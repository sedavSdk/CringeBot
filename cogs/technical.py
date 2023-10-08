from discord.ext import commands
import discord
import sys
sys.path.append("..")
from utils import *

class CogTechnical(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Выключить (скорее всего вы это юзать не можете)')
    async def stop(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            voice_client = discord.utils.get(interaction.bot.voice_clients, guild=interaction.guild)
            if is_connected(voice_client):
                await voice_client.disconnect()
            sys.exit()