from discord.ext import commands
import discord
from discord import app_commands
import configparser
import youtube_dl
import sys
import datetime
import typing
sys.path.append("..")
from utils import *

class CogPlay(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.music = []
        self.now_playing = 0
        self.mode = 0
        config = configparser.ConfigParser()
        config.read('botWB.ini')
        self.logs = config['id']['logs_channel_id']
        self.ban = config['bans']['music_role']
 
    def music_end(self, interaction):
        if self.mode != 2:
            self.now_playing += 1
        self.music_queue(interaction)
    
    def music_queue(self, interaction):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        if self.now_playing >= len(self.music):
            if self.mode >= 1:
                self.now_playing = 0
            else:
                return
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if not voice.is_playing() and not voice.is_paused():
            voice.play(discord.FFmpegPCMAudio(self.music[self.now_playing], **FFMPEG_OPTIONS), after=lambda e: self.music_end(interaction))
    
    @app_commands.command(name="play", description="добавить трек в очередь")
    async def play(self, interaction: discord.Interaction, url : str):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) add to queue {url}')
            await log(interaction, f'{interaction.user} UNSUCCESSFUL(no permission) add to queue {url}', self.logs)
            return
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
            await log(interaction, f'{interaction.user} UNSUCCESSFUL(no voice channel) add to queue {url}', self.logs)
            return
        
        print(f'{datetime.datetime.now()}: {interaction.user} add to queue {url}')
        log(interaction, f'{interaction.user} add to queue {url}', self.logs)
        
        voiceChannel = interaction.user.voice.channel
        voice = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
    
        if not is_connected(voice):
            voice = await voiceChannel.connect()
            await self.clear(interaction)
        if self.now_playing < 0:
            self.now_playing = 0

        if len(self.music) != self.now_playing or voice.is_playing():
            await interaction.response.send_message('добавляю в очередь', ephemeral=True)
        else:
            await interaction.response.send_message('запускаю', ephemeral=True)
        

        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            self.music.append(URL)
            self.music_queue(interaction)
    
    
    
    @app_commands.command(description='Поставить музыку на паузу')
    async def pause(self, interaction: discord.Interaction):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) stop playing')
            log(interaction, f'{interaction.user} UNSUCCESSFUL(no permission) stop playing', self.logs)
            return
        
        print(f'{datetime.datetime.now()}: {interaction.user} stop playing')
        log(interaction, f'{interaction.user} stop playing', self.logs)
        await interaction.response.send_message('пауза', ephemeral=True)
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_playing():
            voice.pause()
    
    @app_commands.command(description='Продолжить проигрывание')
    async def resume(self, interaction: discord.Interaction):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) resume playing')
            log(interaction, f'{interaction.user} UNSUCCESSFUL(no permission) resume playing', self.logs)
            return
        print(f'{datetime.datetime.now()}: {interaction.user} resume playing')
        await interaction.response.send_message('продолжаю', ephemeral=True)
        log(interaction, f'{interaction.user} resume playing', self.logs)
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice.is_paused():
            voice.resume()

    @app_commands.command(description='Пропустить трэк')
    async def skip(self, interaction: discord.Interaction):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) skip track')
            log(interaction, f'{interaction.user} UNSUCCESSFUL(no permission) skip track', self.logs)
            return
        if self.mode == 2:
            self.now_playing +=1
        print(f'{datetime.datetime.now()}: {interaction.user} skip track')
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        log(interaction, f'{interaction.user} skip track', self.logs)
        await interaction.response.send_message('пропускаю', ephemeral=True)
        if voice.is_playing():
            voice.stop()

    @app_commands.command(description='Очистить очередь')
    async def clear(self, interaction: discord.Interaction):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) clear queue')
            log(interaction, f'{interaction.user} UNSUCCESSFUL(no permission) clear queue', self.logs)
            return
        if len(self.music) > 0:
            print(f'{datetime.datetime.now()}: {interaction.user} clear queue')
            voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
            await interaction.response.send_message('чистим чистим чистим', ephemeral=True)
            log(interaction, f'{interaction.user} clear queue', self.logs)
            self.music = []
            self.now_playing = -1
            if voice.is_playing():
                voice.stop()

    @app_commands.command(description='Изменить режим очереди')
    async def mode(self, interaction: discord.Interaction, item: typing.Literal['без повторений', 'с повторениями', 'повтор одной песни']):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) edit mode')
            log(interaction, f'{interaction.user} UNSUCCESSFUL(no permission) edit mode', self.logs)
            return
        new_mode = ['без повторений', 'с повторениями', 'повтор одной песни'].index(item)
        modeMSG = ['no repeat', 'repeat', 'repeat one song']
        modeMSG_RU = ['не повторять', 'повторять', 'повторять одну песню']
        print(f'{datetime.datetime.now()}: {interaction.user} edit mode to {modeMSG[new_mode]}')
        await interaction.response.send_message(f'режим очереди изменен на {modeMSG_RU[new_mode]}', ephemeral=True)
        log(interaction, f'{interaction.user} edit mode to {modeMSG[new_mode]}', self.logs)
        self.mode = new_mode    

    @commands.command(description='Выключить (скорее всего вы это юзать не можете)')
    @commands.has_permissions(administrator=True)
    async def stop(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(interaction.bot.voice_clients, guild=interaction.guild)
        if is_connected(voice_client):
            await voice_client.disconnect()
        sys.exit()

    @app_commands.command(description='Покинуть гс канал')
    async def leave(self, interaction: discord.Interaction):
        if check_ban(interaction, self.ban):
            await interaction.response.send_message('вы не можете использовать команду', ephemeral=True)
            print(f'{datetime.datetime.now()}: {interaction.user} UNSUCCESSFUL(no permission) remove bot from channel')
            log(interaction, f'{interaction.user} UNSUCCESSFUL(no permission) remove bot from channel', self.logs)
            return
        
        
        print(f'{datetime.datetime.now()}: {interaction.user} remove bot from channel')
        log(interaction, f'{interaction.user} remove bot from channel', self.logs)
        await interaction.response.send_message('бб', ephemeral=True)
        voice_client = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
        if self.is_connected(voice_client):
            await voice_client.disconnect()
        
