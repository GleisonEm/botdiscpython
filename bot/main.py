import discord
from discord.ext import commands
from discord.utils import get

# Defina o prefixo de comando e o token do bot.
PREFIX = "!"
TOKEN = ""
AUDIO_FILE = "zap2.mp3"

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

@bot.command(name='play', help='Reproduz um áudio no canal atual')
async def play_audio(ctx):
    print('entrei aq')
    # Verificar se o solicitante está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando!")
        return

    # Pegar o canal de voz do solicitante
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
        voice_client.play(discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source=AUDIO_FILE), after=lambda e: print('Áudio terminou de tocar!', e))

# Iniciar o bot
bot.run(TOKEN)
