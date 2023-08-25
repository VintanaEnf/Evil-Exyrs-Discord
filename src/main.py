import discord
from discord import app_commands
import bard
from spy_fall import spyFall

from textblob import TextBlob
from discord.ext import commands
import sympy as maths

import sys
import const
import temp
import subprocess

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

client = discord.Client(intents=discord.Intents.all())

tree = app_commands.CommandTree(client)

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
    userName = str(message.author)
    userMessage = str(message.content)
    print(f'{userName} : {userMessage}')

    #This line will ignore the messages of itself.
    if message.author == client.user:
        return

    if message.content.startswith(f"{const.bot_prefix}link"):
        await message.channel.send(keys.DISCORD_INVITE)

    if (message.content == (f"{const.bot_prefix}help")) and const.feature_bard:
        embed = discord.Embed(title="Evil Exyrs / Help", description="This discord bot is Exyrs' personal discord bot. \n\n **note**: some commands may not work since features can be enabled or disabled.", color=discord.Color.red())
        embed.add_field(name=f"{const.bot_prefix}bard <message>", value="Calls Google's LLM -> PaLM 2.", inline=False)
        embed.add_field(name=f"{const.bot_prefix}latex <message>", value="Calls Google's LLM and translates the message into LaTeX code.", inline=False)
        embed.add_field(name=f"{const.bot_prefix}math <math equation>", value="Evaluates the mathematical expression, expressions in LaTeX is recommended.", inline=False)
        embed.add_field(name=f"{const.bot_prefix}spyfall <parameter>", value=f"Starts a game of Spyfall. (**quick start**: {const.bot_prefix}spyfall game). \n\n **possible spyfall parameters**: \"game\", \"start\", \"mkmap <map name> <role1> <role2>...\", rmmap <map name>, guess", inline=False)
        await message.channel.send(embed=embed)
        return

    if message.content.startswith(f"{const.bot_prefix}bard") and const.feature_bard:
        answer = bard.talkShort(userMessage)
        await message.channel.send(answer)
        return
    
    if message.content.startswith(f"{const.bot_prefix}latex") and const.feature_bard:
        answer = bard.latexify(userMessage.split('$')[1])
        await message.channel.send(answer)
        return

    #Problems: I don't know how to turn latex into sympy usable form and return the proper answer.
    if message.content.startswith(f"{const.bot_prefix}math") and const.feature_math:
        eq = userMessage.split("math")[1]
        parsed_eq = maths.latex(eq)
        result = parsed_eq
        await message.channel.send(result)
        return
    
    #todo update spyfall

    #spyfall game command specific.
    if message.content.startswith(f"{const.bot_prefix}spyfall") and const.feature_spyfall:
        global process_dictionary
        if message.content == f"{const.bot_prefix}spyfall game":
            embed = discord.Embed(title="Spyfall", description=f"A game of spyfall has been started by {userName}", color=discord.Color.blue())
            embed.add_field(name="How to play?", value=" 1. React 🕵️ to join.\n 2. A location and role will be sent to you in private. \n 3. The player who was recently asked is the  one asking next. \n 4. The spy will need to guess your location in order for him to win. \n 5. $spyfall start", inline=False)
            temp.spyfall_game = await message.channel.send(embed=embed)
            await temp.spyfall_game.add_reaction("🕵️")
            process_dictionary.update({message.guild : spyFall(message.author.id, message.guild)})
            return
        
        if message.content == f"{const.bot_prefix}spyfall start":
            spyfall = process_dictionary[message.guild]
            play : list = spyfall.showplayers()
            await message.channel.send(f"debug, the spy is: {client.get_user(spyfall.start())}")
            for i in play:
                user = client.get_user(i)
                await user.send("Welcome to SpyFall")
                role = spyfall.getrole(i)
                await user.send(f"**{spyfall.getmap(role)}**")
                await user.send(f"Your role is: {role}")
            return
        
        if message.content == f"{const.bot_prefix}spyfall maps":
            spyfall = process_dictionary[message.guild]
            currentgamemaps = spyfall.maps()
            embed = discord.Embed(title="Spyfall Map Collection", description=f"All maps created in {message.guild}.", color=discord.Color.blue())
            cmaps :str = ""
            for keya in currentgamemaps:
                cmaps = f"{cmaps}* {keya}\n"
            embed.add_field(name="Maps:", value=cmaps, inline=False)
            temp.spyfall_game = await message.channel.send(embed=embed)
            return
        
        if message.content == f"{const.bot_prefix}spyfall players":
            spyfall = process_dictionary[message.guild]
            currentplayers = spyfall.showplayers()
            embed = discord.Embed(title="Spyfall players", description=f"All current players in {message.guild}.", color=discord.Color.blue())
            cmaps :str = ""
            for keya in currentplayers:
                cmaps = f"{cmaps}* {client.get_user(keya)}\n"
            embed.add_field(name="Players:", value=cmaps, inline=False)
            temp.spyfall_game = await message.channel.send(embed=embed)
            return
        
        if message.content.startswith(f"{const.bot_prefix}spyfall mkmap "):
            messageonly = userMessage.split("mkmap ")[1]
            listtemp : list = []
            spyfall = process_dictionary[message.guild]
            t = messageonly.split(", ")
            for i in t:
                listtemp.append(i)
            listtemp.append("spy")
            mapname = listtemp[0]
            listtemp.remove(listtemp[0])
            spyfall.addmap(mapname, listtemp)
            await message.channel.send(f"Successfully added **{mapname}** containing **{listtemp}** in maps list.")
            return

        if message.content.startswith(f"{const.bot_prefix}spyfall rmmap "):
            array = userMessage.split(" ")
            spyfall = process_dictionary[message.guild]
            await message.channel.send(f"Successfully removed **{array[2]}** containing **{spyfall.removemap(array[2])}** in maps list.")
            return

@client.event
async def on_reaction_add(reaction, user):
    global process_dictionary
    constraints: bool =  user != client.user and isinstance(reaction.message.channel, discord.TextChannel)
    constraints = constraints and reaction.message.author == client.user and reaction.emoji == "🕵️"
    if constraints:
        spyfall = process_dictionary[user.guild]
        if not spyfall.addplayer(user.id):
            await reaction.message.channel.send(f"{user.name} is already in the Spyfall game.")
            return
        else:
            await reaction.message.channel.send(f"{user.name} joined the Spyfall game.")
            return



@tree.command(name="hello", description="Says hello")
async def hello(interaction):
    await interaction.response.send("Hello!")

def correctThis(text):
    return TextBlob(text).correct()

client.run(keys.DISCORD_TOKEN)
