from discord.ext import commands
import discord
from discord import app_commands
import youtube_dl
import sys
sys.path.append("..")
from utils import is_connected

class CogPlay(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.music = []
        self.now_playing = 0
 
    def music_end(self, interaction):
        self.now_playing += 1
        self.music_queue(interaction)
        print(self.music, self.now_playing)
    
    def music_queue(self, interaction):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        if self.now_playing >= len(self.music):
            return
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if not voice.is_playing() and not voice.is_paused():
            voice.play(discord.FFmpegPCMAudio(self.music[self.now_playing], **FFMPEG_OPTIONS), after=lambda e: self.music_end(interaction))
    
    @app_commands.command(name="play", description="123")
    async def play(self, interaction: discord.Interaction, url : str):
        print(interaction.user.roles)
        ydl_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
    
            }]
        }
        
        
        if interaction.user.voice == None:
            await interaction.response.send_message("Зайди в канал, дибила кусок", ephemeral=True)
            return
        
        
        voiceChannel = interaction.user.voice.channel
        voice = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
    
        if not is_connected(voice):
            voice = await voiceChannel.connect()

        if len(self.music) == self.now_playing or voice.is_playing():
            await interaction.response.send_message('добавляю в очередь', ephemeral=True)
        else:
            await interaction.response.send_message('запускаю', ephemeral=True)
        

        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            self.music.append(URL)
            self.music_queue(interaction)
    
    @app_commands.command(description='Покинуть гс канал')
    async def leave(self, interaction: discord.Interaction):
        await interaction.response.send_message('бб')
        voice_client = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
        if self.is_connected(voice_client):
            await voice_client.disconnect()
    
    @app_commands.command(description='Поставить музыку на паузу')
    async def pause(self, interaction: discord.Interaction):
        await interaction.response.send_message('пауза', ephemeral=True)
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_playing():
            voice.pause()
    
    @app_commands.command(description='Продолжить проигрывание')
    async def resume(self, interaction: discord.Interaction):
        await interaction.response.send_message('продолжаю', ephemeral=True)
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_paused():
            voice.resume()

    @app_commands.command(description='Пропустить трэк')
    async def skip(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        await interaction.response.send_message('пропускаю', ephemeral=True)
        if voice.is_playing():
            voice.stop()

    @app_commands.command(description='Очистить очередь')
    async def clear(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        await interaction.response.send_message('чистим чистим чистим', ephemeral=True)
        self.music = []
        self.now_playing = -1
        if voice.is_playing():
            voice.stop()
    

    