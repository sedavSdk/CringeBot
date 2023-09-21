import discord
from youtube_dl import YoutubeDL
from asyncio import sleep
import nacl
from decouple import config


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


music_queue = []

da = "gadost21"
@bot.command()
async def play_music(ctx, arg):
    global vc
    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except:
        print('Уже подключен или не удалось подключиться')

    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')

    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)

        URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))
                
        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!play'):

        url = message.content[6:]
        music_queue.append(url)

        if message.author.voice and message.author.voice.channel:
            if not message.guild.voice_client:
                await play_music(message, music_queue.pop(0))


client.run(config('TOKEN'))
