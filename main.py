import discord
from discord.ext import commands
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
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
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
async def play(ctx, url : str):
    global music, now_playing
    ydl_options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
 
        }]
    }
    
    
    if ctx.message.author.voice == None:
        await ctx.send("Зайди в канал, дибила кусок")
        return
    
    voiceChannel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
 
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
            music_queue(ctx)
            
 
@client.tree.command(description='Покинуть гс канал')
async def leave(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    print("da1")
    if is_connected(voice_client):
        print("da2")
        await voice_client.disconnect()
 
@client.tree.command(description='Поставить музыку на паузу')
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
 
@client.tree.command(description='Продолжить проигрывание')
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
 
@client.tree.command(description='Выключить (скорее всего вы это юзать не можете)')
async def stop(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if is_connected(voice_client):
        await voice_client.disconnect()
    sys.exit()
 
 
client.run(config('TOKEN'))