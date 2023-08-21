import discord
import bard
import const

# ------------------------------------------------------------------
#The location of keys in my machine:
import sys
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


from textblob import TextBlob
from discord.ext import commands

client = discord.Client()

#This will run when the bot begins.
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

    if message.content.startswith("link"):
        await message.channel.send(keys.DISCORD_LINK)

    if message.content.startswith("Bard "):
        # talk = userMessage.split('\"')[1]
        talk=userMessage
        await message.channel.send(bard.talkLong(talk))
        return
    
    if message.content.startswith("latex "):
        talk = userMessage.split('\"')[1]
        await message.channel.send(bard.latexify(talk))
        return
    
def correctThis(text):
    return TextBlob(text).correct()

client.run(keys.DISCORD_TOKEN)