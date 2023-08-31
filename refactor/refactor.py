import discord
from discord import app_commands
from discord.ext import commands
import const
import sys
import os
if const.feature_bard:
    import bard

if const.feature_spyfall:
    from spy_fall import spyFall

if const.feature_textblob:
    from textblob import TextBlob

if const.feature_math:
    import sympy as maths


#todo: turn this into keys.json
# ------------------------------------------------------------------
#The location of keys in my machine:
sys.path.append(const.keys_location)
import keys
#
# The keys.py contains variables holding API keys and Tokens.
#
# Here are the variables:
# PALM = Generative Language Client API Key.
# GPT = ChatGPT API key.
# DISCORD_TOKEN = My Discord Token.
# DISCORD_INVITE = Contains the invite link of my Discord Bot.
# ------------------------------------------------------------------

bot = commands.Bot(command_prefix='!',help_command=None, intents=discord.Intents.all())



#this dictionary will contain all of the processes in each guild.

async def load_cogs():
    absolute_path = os.path.abspath(__file__)
    path = os.path.join(os.path.dirname(absolute_path), f"cogs")
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

#This will run when the bot begins.
print("The bot is NOW starting, please wait...")

@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))
    load_cogs()

@bot.event
async def on_message(message):

    #this line breaks up the message as userName and userMessage
    userName = str(message.author)
    userMessage = str(message.content)
    print(f'{userName} in {message.guild}: {userMessage}')
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")
    return

@bot.command()
async def link(ctx):
    await ctx.send(keys.DISCORD_INVITE)


bot.run(keys.DISCORD_TOKEN)