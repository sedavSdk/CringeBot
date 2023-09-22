import discord
from discord.ext import commands
import youtube_dl
import os, sys
import asyncio
from decouple import config
 
intents = discord.Intents.default()
intents.message_content = True
 
client = commands.Bot(command_prefix='!', intents=intents)
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
 
@client.command()
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
            
 
@client.command()
async def leave(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    print("da1")
    if is_connected(voice_client):
        print("da2")
        await voice_client.disconnect()
 
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
 
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
 
@client.command()
async def stop(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if is_connected(voice_client):
        await voice_client.disconnect()
    sys.exit()
 
 
client.run(config('TOKEN'))