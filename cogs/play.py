from discord.ext import commands
import discord
from discord import app_commands
import configparser
import youtube_dl
import sys
import datetime
sys.path.append("..")
from utils import *

class CogPlay(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.music = []
        self.now_playing = 0
        config = configparser.ConfigParser()
        config.read('botWB.ini')
        self.ban = config['bans']['music_role']
 
    def music_end(self, interaction):
        self.now_playing += 1
        self.music_queue(interaction)
    
    def music_queue(self, interaction):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        if self.now_playing >= len(self.music):
            return
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if not voice.is_playing() and not voice.is_paused():
            voice.play(discord.FFmpegPCMAudio(self.music[self.now_playing], **FFMPEG_OPTIONS), after=lambda e: self.music_end(interaction))
    
    @app_commands.command(name="play", description="добавить трек в очередь")
    async def play(self, interaction: discord.Interaction, url : str):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) add to queue {url}')
            return

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
            await interaction.response.send_message("Зайди в канал, дибила кусок", ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no voice channel) add to queue {url}')
            return
        await interaction.response.send_message('включаю', ephemeral=True)

        
        voiceChannel = interaction.user.voice.channel
        voice = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
    
        if not is_connected(voice):
            voice = await voiceChannel.connect()

        if len(self.music) != self.now_playing or voice.is_playing():
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
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            return
        
        print(f'{datetime.datetime.now()}: {interaction.user} remove bot from channel')
        await interaction.response.send_message('бб', ephemeral=True)
        voice_client = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
        if self.is_connected(voice_client):
            await voice_client.disconnect()
    
    @app_commands.command(description='Поставить музыку на паузу')
    async def pause(self, interaction: discord.Interaction):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) stop playing')
            return
        
        print(f'{datetime.datetime.now()}: {interaction.user} stop playing')
        await interaction.response.send_message('пауза', ephemeral=True)
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_playing():
            voice.pause()
    
    @app_commands.command(description='Продолжить проигрывание')
    async def resume(self, interaction: discord.Interaction):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) resume playing')
            return
        print(f'{datetime.datetime.now()}: {interaction.user} resume playing')
        await interaction.response.send_message('продолжаю', ephemeral=True)
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_paused():
            voice.resume()

    @app_commands.command(description='Пропустить трэк')
    async def skip(self, interaction: discord.Interaction):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) skip track')
            return
        print(f'{datetime.datetime.now()}: {interaction.user} skip track')
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        await interaction.response.send_message('пропускаю', ephemeral=True)
        if voice.is_playing():
            voice.stop()

    @app_commands.command(description='Очистить очередь')
    async def clear(self, interaction: discord.Interaction):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) clear queue')
            return
        print(f'{datetime.datetime.now()}: {interaction.user} clear queue')
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        await interaction.response.send_message('чистим чистим чистим', ephemeral=True)
        self.music = []
        self.now_playing = -1
        if voice.is_playing():
            voice.stop()
    
