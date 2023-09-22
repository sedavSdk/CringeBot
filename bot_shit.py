import discord
from discord.ext import commands

def is_connected(voice_client):
    return voice_client and voice_client.is_connected()