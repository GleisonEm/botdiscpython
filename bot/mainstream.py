import os

import discord
import requests
from discord.ext import commands
from discord.utils import get

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

@bot.command()
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.stop()

@bot.command()
async def play(ctx, url):
    print('entrei aq')
    # Verificar se o solicitante está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando!")
        return

    api_url = 'http://localhost:3000/download'
    response = requests.get(api_url, params={'url': url}, stream=True)
    print("status code", response.status_code)
    if response.status_code == 200:
        channel = ctx.message.author.voice.channel

        # Conectar ao canal de voz
        voice_client = get(bot.voice_clients, guild=ctx.guild)
        if voice_client is None:
            await channel.connect()
            voice_client = get(bot.voice_clients, guild=ctx.guild)

        elif voice_client.is_connected():
            await voice_client.move_to(channel)

        # Reproduzir o arquivo de audio no canal de voz
        if not voice_client.is_playing():
            voice_client.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=response.raw, pipe=True), after=lambda e: print('Áudio terminou de tocar!', e))

print(os.environ.get('TOKEN_DISCORD'))
# Iniciar o bot
bot.run(TOKEN)
