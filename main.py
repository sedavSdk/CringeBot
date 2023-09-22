import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import app_commands
import youtube_dl
import os, sys
import asyncio
from decouple import config
 
intents = discord.Intents.default()
intents.message_content = True
MY_GUILD = discord.Object(id=318051378972983297)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix='/', intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
 
client = MyClient(intents=intents)
music = []
now_playing = 0

 
def is_connected(voice_client):
    return voice_client and voice_client.is_connected()
 
def music_end(ctx):
    global music, now_playing
    now_playing += 1
    music_queue(ctx)
 
def music_queue(ctx):
    global music, now_playing
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if now_playing >= len(music):
        return
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio(music[now_playing], **FFMPEG_OPTIONS), after=lambda e: music_end(ctx))
 
@client.tree.command(description='Включить музыку (очевидно)')
@app_commands.describe(
    url='ссылка на ютуб'
)
async def play(interaction: discord.Interaction, url : str):
    await interaction.response.send_message('включаю')
    global music, now_playing
    ydl_options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
 
        }]
    }
    
    
    if interaction.user.voice == None:
        await interaction.send("Зайди в канал, дибила кусок")
        return
    
    voiceChannel = interaction.user.voice.channel
    voice = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
 
    if not is_connected(voice):
        voice = await voiceChannel.connect()
 
    
    if voice == None:
        print("pizda")
    else:
        
        print("da1")
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            print("da2")
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            music.append(URL)
            music_queue(interaction)
            
 
@client.tree.command(description='Покинуть гс канал')
async def leave(interaction: discord.Interaction):
    await interaction.response.send_message('бб')
    voice_client = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
    print("da1")
    if is_connected(voice_client):
        print("da2")
        await voice_client.disconnect()
 
@client.tree.command(description='Поставить музыку на паузу')
async def pause(interaction: discord.Interaction):
    await interaction.response.send_message('пауза')
    voice = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if voice.is_playing():
        voice.pause()
 
@client.tree.command(description='Продолжить проигрывание')
async def resume(interaction: discord.Interaction):
    await interaction.response.send_message('продолжаю')
    voice = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if voice.is_paused():
        voice.resume()
 
@client.tree.command(description='Выключить (скорее всего вы это юзать не можете)')
@has_permissions(manage_roles=True, ban_members=True)
async def stop(interaction: discord.Interaction):
    await interaction.response.send_message('я в ахуе')
    voice_client = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
    if is_connected(voice_client):
        await voice_client.disconnect()
    sys.exit()
 
 
client.run(config('TOKEN'))