import os

import discord
import requests
from discord.ext import commands
from discord.utils import get
import yt_dlp as youtube_dl
import json

# Defina o prefixo de comando e o token do bot.
PREFIX = "jorg"
TOKEN = os.environ.get('TOKEN_DISCORD')
AUDIO_FILE = "audio.mp3"

# Intencoes do bot (permitir uso de membros, etc).
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

# Crie um objeto 'bot'
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} conectou ao Discord!')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ydl = youtube_dl.YoutubeDL(ydl_opts)  # Create the YoutubeDL object outside the command

@bot.command()
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando!")
        return

    channel = ctx.author.voice.channel

    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        await channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)
    elif voice_client.is_connected():
        await voice_client.move_to(channel)

    with ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_url = info_dict.get('url')

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -acodec pcm_s16le -f s16le -ar 48000 -ac 2',
        }

        voice_client.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=audio_url, **ffmpeg_options), after=lambda e: print('Áudio terminou de tocar!', e))


@bot.command()
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.stop()
    await ctx.send("Reprodução de áudio interrompida.")

print(os.environ.get('TOKEN_DISCORD'))
# Iniciar o bot
bot.run(TOKEN)
