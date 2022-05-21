from youtube_dl import YoutubeDL
from nextcord import FFmpegPCMAudio, member
from nextcord.ext import commands
from btoken import btoken
import requests
import random

client = commands.Bot(command_prefix="*")
channel, voice = None, None


@client.event
async def on_ready():
    global ista, istajson
    ista = requests.request('GET', 'http://localhost:8080/ista')
    istajson = ista.json()
    print("bot is online")


@client.command()
async def join(ctx):
    global channel, voice
    if not channel:
        channel = ctx.message.author.voice.channel
    if not voice:
        voice = await channel.connect()
    if voice and voice.is_connected():
        await voice.moveto(channel)
    else:
        voice = await channel.connect()


@client.command()
async def play(ctx, url):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }
    global channel, voice
    if not channel:
        channel = ctx.message.author.voice.channel
    if not voice:
        voice = await channel.connect()
    if not voice.is_playing():
        with YoutubeDL(YTDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info["url"]
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send("Bot is playing")


@client.command()
async def stop(ctx):
    global channel, voice
    if not channel:
        channel = ctx.message.author.voice.channel
    if not voice:
        voice = await channel.connect()

    if voice.is_playing():
        voice.stop()
        await ctx.send("Stopping...")


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

    # todo: tictactoe


@client.command()
async def msiakman(ctx, mention: member = None):
    words = tuple(istajson)
    if mention:
        print(type(member))
        index = random.randrange(0, len(words))
        await mention.edit(nick=f'Msiak {words[index]}')
        await ctx.send("Done")
    else:
        await ctx.send('Oznacz msiaka')


@client.command()
async def msiakista(ctx, count: int = 1):
    words = tuple(istajson)
    for i in range(count):
        index = random.randrange(0, len(words))
        await ctx.send(f'Msiak {words[index]}')


client.run(btoken)
