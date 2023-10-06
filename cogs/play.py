from discord.ext import commands
import discord
from discord import app_commands
import youtube_dl
import sys
import datetime
sys.path.append("..")
from utils import is_connected

class CogPlay(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.music = []
        self.now_playing = 0
 
    def music_end(self, ctx):
        self.now_playing += 1
        self.music_queue(ctx)
    
    def music_queue(self, ctx):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        if self.now_playing >= len(self.music):
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(self.music[self.now_playing], **FFMPEG_OPTIONS), after=lambda e: self.music_end(ctx))
    
    @app_commands.command(name="play", description="добавить трек в очередь")
    async def play(self, interaction: discord.Interaction, url : str):
        print(f'{datetime.datetime.now()}: {interaction.user} add to queue {url}')
        ydl_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
    
            }]
        }
        
        
        if interaction.user.voice == None:
            await interaction.response.send_message("Зайди в канал, дибила кусок")
            return
        await interaction.response.send_message('включаю')
        voiceChannel = interaction.user.voice.channel
        voice = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
    
        if not is_connected(voice):
            voice = await voiceChannel.connect()
        
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            self.music.append(URL)
            self.music_queue(interaction)
    
    @app_commands.command(description='Покинуть гс канал')
    async def leave(self, interaction: discord.Interaction):
        print(f'{datetime.datetime.now()}: {interaction.user} remove bot from channel')
        await interaction.response.send_message('бб')
        voice_client = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
        if self.is_connected(voice_client):
            await voice_client.disconnect()
    
    @app_commands.command(description='Поставить музыку на паузу')
    async def pause(self, interaction: discord.Interaction):
        print(f'{datetime.datetime.now()}: {interaction.user} stop playing')
        await interaction.response.send_message('пауза')
        voice = discord.utils.get(self, self.client.voice_clients, guild=interaction.guild)
        if voice.is_playing():
            voice.pause()
    
    @app_commands.command(description='Продолжить проигрывание')
    async def resume(self, interaction: discord.Interaction):
        print(f'{datetime.datetime.now()}: {interaction.user} resume playing')
        await interaction.response.send_message('продолжаю')
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_paused():
            voice.resume()

    

    