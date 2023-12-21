import os

import discord
import requests
from discord.ext import commands
from discord.utils import get

PREFIX = "jorg"
TOKEN = os.environ.get('TOKEN_DISCORD')
AUDIO_FILE = "audio.mp3"

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} conectou ao Discord!')

@bot.command()
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.stop()

@bot.command()
async def play(ctx, url):
    print('entrei aq')

    if ctx.author.voice is None:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando!")
        return

    api_url = 'http://192.168.0.106:3000/download'
    response = requests.get(api_url, params={'url': url}, stream=True)
    if response.status_code == 200:

        with open(AUDIO_FILE, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                else:
                    print(f'Erro na requisição. Código de status: {response.status_code}')
                    print(response.text)

    channel = ctx.message.author.voice.channel

    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        await channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)

    elif voice_client.is_connected():
        await voice_client.move_to(channel)

    if not voice_client.is_playing():
        voice_client.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=AUDIO_FILE), after=lambda e: print('Áudio terminou de tocar!', e))
#
bot.run(TOKEN)
