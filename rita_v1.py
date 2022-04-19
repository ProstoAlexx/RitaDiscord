import discord
from http import client
from logging import error
from unicodedata import name
import asyncio
from discord.ext import commands

client = commands.Bot(command_prefix='_')

token = "OTY1NjgxMTg1NzY0MzA3MDE2.Yl2usA.7k-v2G3-pPVWo5O5KCLmD1khs7U"

curseWord = ['6ля']

HowMany = ['сколько см у Андрея']

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
   


@client.event
async def on_command_error(ctx, error):
    if isistance(error, commands.MissingRequiredArgument):
        await ctx.send('я тебя не понимаю, лол')
    if isistance(error, commands.MissingPremission):
        await ct.send('простым смертным такое не дозволено)')
       
@client.command()
async def info(ctx):
    await ctx.send('список всего что я пока что умею: _rank - твой ранг на сервере, _tea - дам тебе чай, _coffee - дам тебе коффе <3')

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
