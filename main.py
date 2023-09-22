import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import app_commands
import youtube_dl
import os, sys
import asyncio
import json
from decouple import config
 
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
MY_GUILD = discord.Object(id=318051378972983297)

class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
 
client = MyClient(intents=intents)
music = []
now_playing = 0


bot_log = 'bot-logs'
isLog = True

WHITELIST = 0
BLACKLIST = 1

roles = [[], []]
roles_status = WHITELIST
users = [[], []]
users_status = WHITELIST
channels = [[], []]
channels_status = BLACKLIST

async def log(ctx, message):
    global isLog, bot_log
    if isLog:
        channel1 = discord.utils.get(ctx.guild.channels, name=bot_log)
        print(channel1)
        await channel1.send(message)

def check_role(ctx):
    user = ctx.author
    if user.guild_permissions.administrator:
        return True
    if roles_status == WHITELIST:
        for role in user.roles:
            if role in roles[WHITELIST]:
                return True
        return False
    else:
        for role in user.roles:
            if role in roles[BLACKLIST]:
                return False
        return True
    
def check_user(ctx):
    user = ctx.author
    if user.guild_permissions.administrator:
        return True
    if users_status == WHITELIST:
        return user in users[WHITELIST]
    else:
        return user not in users[BLACKLIST]
        
def check_channel(ctx):
    channel = ctx.channel
    if channels_status == WHITELIST:
        return channel in channels[WHITELIST]
    else:
        return channel not in channels[BLACKLIST]
        


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

@client.event
async def on_ready():
    global roles, users, channels, roles_status, users_status, channels_status
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            roles = data['roles']
            roles_status = data['roles_status']
            users = data['users']
            channels = data['channels']
    except:
        pass
 
@client.tree.command(description='Включить музыку (очевидно)')
@app_commands.describe(
    url='ссылка на ютуб'
)
async def play(interaction: discord.Interaction, url : str):
    print(interaction.user.roles)
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
 

@commands.has_role('botMaster')
@client.command(description='Выключить (скорее всего вы это юзать не можете)')
async def stop(ctx):
    global roles, users, channels, roles_status, users_status, channels_status
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if is_connected(voice_client):
        await voice_client.disconnect()
    with open('data.json', 'w') as f:
        data = {
            'users': users,
            'users_status': users_status,
            'roles': roles,
            'roles_status': roles_status,
            'channels': channels,
            'channels_status': channels_status
        }
        json.dump(data, f)
        
    sys.exit()

@client.command()
async def access(ctx, accessList, typeList, data):
    global roles, users, channels, roles_status, users_status, channels_status
    if accessList.lower() in ["users", "roles", "channels"]:
        edit = [users, roles, channels][["users", "roles", "channels"].index(accessList.lower())]
        if typeList.lower() in ["whitelist", "blacklist"]:
            wl = [WHITELIST, BLACKLIST][["whitelist", "blacklist"].index(typeList.lower())]
            edit[wl].append(data)
        else:
            ctx.send("Неправильный тип, используйте whitelist или blacklist")
    else:
        ctx.send("Неправильный список, используйте users, roles или channels")

@client.command()
async def changeAccess(ctx, accessList):
    global roles, users, channels, roles_status, users_status, channels_status
    if accessList.lower() in ["users", "roles", "channels"]:
        accessList = accessList.lower()
        message = str(ctx.author) + ' изменил тип {} с '.format(accessList)
        if accessList == "users":
            message += ['whitelist', 'blacklist'][users_status]
            users_status = (users_status + 1) % 2
            message += ' на ' + ['whitelist', 'blacklist'][users_status]
        elif accessList == "roles":
            message += ['whitelist', 'blacklist'][roles_status]
            roles_status = (roles_status + 1) % 2
            message += ' на ' + ['whitelist', 'blacklist'][roles_status]
        elif accessList == "channels":
            message += ['whitelist', 'blacklist'][channels_status]
            channels_status = (channels_status + 1) % 2
            message += ' на ' + ['whitelist', 'blacklist'][channels_status]
        await log(ctx, message)
    else:
        ctx.send("Неправильный список, используйте users, roles или channels")
        
    


@client.command()
async def test(ctx):
    print(str(ctx.author), str(ctx.author) == "Taiko")
                


    
 
 
client.run(config('TOKEN'))