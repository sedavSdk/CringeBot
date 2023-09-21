import discord
import youtube_dl
import asyncio
import nacl

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


music_queue = []


async def play_music(ctx, url):
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print(url)
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']

    voice_client.play(discord.FFmpegPCMAudio(url2))
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()


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


client.run('MTE1NDM5NTAxMzYwNjgxMzg1Ng.GNJlRS.TLV_4-Wk2133-yDKpPdb7FNM2zJPyz0OdthZYk')