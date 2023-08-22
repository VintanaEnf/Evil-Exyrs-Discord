import discord
import bard

from textblob import TextBlob
from discord.ext import commands

import sys
import const

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


client = discord.Client()
clipboard = ""
#This will run when the bot begins.
print("The bot is NOW starting, please wait...")
@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

#receives message.
@client.event
async def on_message(message):

    #this line breaks up the message as userName and userMessage
    userName = str(message.author).split('#')[0]
    userMessage = str(message.content)
    print(f'{userName} : {userMessage}')

    #This line will ignore the messages of itself.
    if message.author == client.user:
        return

    if message.content.startswith(f"{const.bot_prefix}link"):
        await message.channel.send(keys.DISCORD_INVITE)

    if message.content.startswith(f"{const.bot_prefix}bard ") and const.feature_bard:
        answer = bard.talkLong(userMessage.split(f'{const.bot_prefix}bard')[1])+""
        await message.channel.send(answer)
        return
    
    if message.content.startswith(f"{const.bot_prefix}latex") and const.feature_bard:
        answer = bard.latexify(userMessage.split('$')[1])
        await message.channel.send(answer)
        return
    
def correctThis(text):
    return TextBlob(text).correct()

client.run(keys.DISCORD_TOKEN)