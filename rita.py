import discord
from http import client
from logging import error
from unicodedata import name
import asyncio
import time
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import youtube_dl

load_dotenv()
# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='_',intents=intents)

token = "OTY1NjgxMTg1NzY0MzA3MDE2.Yl2usA.79THxHq8g1S47vgkqmJe-YRk6OY"

curseWord = ['херово']

@client.event
async def on_ready():
    print("я готов!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="_info"))

@client.listen('on_message')
async def i_wanna_listen(message):
    msg_content = message.content.lower()
    if any(word in msg_content for word in curseWord):
        await message.delete()
        await message.channel.send(f"{message.author.mention} не ругайся пожалуйста, не всем это нравится")
    else:
        return

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@client.event
async def on_command_error(ctx, error):
    if isistance(error, commands.MissingRequiredArgument):
        await ctx.send('я тебя не понимаю, лол')
    if isistance(error, commands.MissingPremission):
        await ct.send('простым смертным такое не дозволено)')
       
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} сначала подключись к голосовому каналу".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("запустите меня сначала в войс")
       
@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Сейчас играет:** {}'.format(filename))
    except:
        await ctx.send("запустите меня сначала в войс")
@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("я еще ничего не включил")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("ничего не играет, используй комманду play_song")
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("я еще ничего не включил")
       
@client.command()
async def info(ctx):
    await ctx.send('список всего что я пока что умею: _rank - твой ранг на сервере, _nom - я кушаю, _tea - дам тебе чай <3')

@client.command()
async def rank(ctx):
    await ctx.send('твой ранг - ')

@client.command()
async def tea(ctx):
    await ctx.send('ты хочешь чай? на, я для тебя тоже заварил :tea:')

@client.command()
async def coffee(ctx):
    await ctx.send('не понимаю, как вы пьете это кофе? :coffee:')

client.run(token)
