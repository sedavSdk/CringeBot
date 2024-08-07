from discord.ext import commands
import datetime
import configparser
import sys
sys.path.append("..")
from utils import doImage
import discord
from random import choice
from discord import app_commands

class CogStatus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.CustomActivity(name="Заработает в четверг"))