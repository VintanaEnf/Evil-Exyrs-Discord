import discord
import bard
from spy_fall import spyFall

from textblob import TextBlob
from discord.ext import commands

import sys
import const

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


client = discord.Client()

#this dictionary will contain all of the processes in each guild.
process_dictionary = {}


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

    if (message.content == (f"{const.bot_prefix}help")) and const.feature_bard:
        embed = discord.Embed(title="Evil Exyrs / Help", description="This discord bot is Exyrs' personal discord bot. \n\n **note**: some commands may not work since features can be enabled or disabled.", color=discord.Color.red())
        embed.add_field(name=f"{const.bot_prefix}bard <message>", value="Calls Google Bard the AI.", inline=False)
        embed.add_field(name=f"{const.bot_prefix}latex <message>", value="Calls Google Bard AI and translates the message into LaTeX code.", inline=False)
        embed.add_field(name=f"{const.bot_prefix}wolframalpha <math equation>", value="Calls WolframAlpha, expressions in LaTeX is recommended.", inline=False)
        embed.add_field(name=f"{const.bot_prefix}spyfall <parameter>", value=f"Starts a game of Spyfall. (**quick start**: {const.bot_prefix}spyfall game).", inline=False)
        await message.channel.send(embed=embed)
        return

    if message.content.startswith(f"{const.bot_prefix}bard") and const.feature_bard:
        answer = bard.talkLong(userMessage.split(f'{const.bot_prefix}bard')[1])+""
        await message.channel.send(answer)
        return
    
    if message.content.startswith(f"{const.bot_prefix}latex") and const.feature_bard:
        answer = bard.latexify(userMessage.split('$')[1])
        await message.channel.send(answer)
        return

    if message.content.startswith(f"{const.bot_prefix}wolframalpha") and const.feature_wolframalpha:
        answer = bard.talkLong(userMessage.split(f'{const.bot_prefix}bard')[1])+""
        await message.channel.send(answer)
        return
    
    #todo update spyfall

    #spyfall game command specific.
    if message.content.startswith(f"{const.bot_prefix}spyfall") and const.feature_spyfall:
        global process_dictionary

        if message.content == f"{const.bot_prefix}spyfall game":
            embed = discord.Embed(title="Spyfall", description=f"A game of spyfall has been started by {userName}", color=discord.Color.blue())
            embed.add_field(name="How to play?", value="1. React 🕵️ to join.\n 2. A location and role will be sent to you in private. \n 3. The player who was recently asked is the  one asking next. \n 4. The spy will need to guess your location in order for him to win. \n 5. Goodluck, have fun.", inline=False)
            const.spyfall_game = await message.channel.send(embed=embed)
            await const.spyfall_game.add_reaction("🕵️")
            process_dictionary.update({message.guild : spyFall(userName, message.guild)})
            return
        
        if message.content == f"{const.bot_prefix}spyfall start":
            return
        
        if message.content == f"{const.bot_prefix}spyfall maps":
            spyfall = process_dictionary[message.guild]
            currentgamemaps = spyfall.maps()
            for keya in currentgamemaps:
                await message.channel.send(keya)
                print(keya)
            return
        
        if message.content.startswith(f"{const.bot_prefix}spyfall addmap "):
            array = userMessage.split(" ")
            listtemp : list = []
            spyfall = process_dictionary[message.guild]
            ctr = 0
            for i in array:
                if ctr >= 3:
                    listtemp.append(i)
                ctr = ctr+1
                    
            spyfall.addmap(array[2], listtemp)
            return
    
@client.event
async def on_reaction_add(reaction, user):
    global process_dictionary
    constraints: bool =  user != client.user and isinstance(reaction.message.channel, discord.TextChannel)
    constraints = constraints and reaction.message.author == client.user and reaction.emoji == "🕵️"
    if constraints:
        spyfall = process_dictionary[user.guild]
        if not spyfall.addplayer(user.name):
            await reaction.message.channel.send(f"{user.name} is already in the Spyfall game.")
            await reaction.message.channel.send(user.guild)
            return
        else:
            await reaction.message.channel.send(f"{user.name} joined the Spyfall game.")
            return



def correctThis(text):
    return TextBlob(text).correct()

client.run(keys.DISCORD_TOKEN)
