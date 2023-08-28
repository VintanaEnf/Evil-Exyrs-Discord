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

client = discord.Client(intents=discord.Intents.all())


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
    global process_dictionary

    #this line breaks up the message as userName and userMessage
    userName = str(message.author)
    userMessage = str(message.content)
    print(f'{userName} in {message.guild}: {userMessage}')

    #This line will ignore the messages of itself.
    if message.author == client.user:
        return

    if message.content.startswith(f"{const.bot_prefix}link"):
        await message.channel.send(keys.DISCORD_INVITE)

    if (message.content == (f"{const.bot_prefix}help")) and const.feature_bard:
        embed = discord.Embed(title="Evil Exyrs / Help", description="These are the commands available for this bot." 
                              "\n\n **note**: some commands may not work since features can be enabled or disabled.", color=discord.Color.red())
        # embed.add_field(name=f"{const.bot_prefix}math <math equation>", value="Evaluates the mathematical expression, expressions in LaTeX is recommended.", inline=False)
        embed.add_field(name=f"🕵🏻 {const.bot_prefix}spyfall <parameter>", value=f"Starts a game of Spyfall. (**quick start**: {const.bot_prefix}spyfall game)." 
                        "\n\n **possible spyfall parameters**: \"game\", \"start\"," 
                        "\"mkmap <map name> <role1> <role2>...\", \"rmmap <map name>\", \"reveal\"", inline=False)
        embed.add_field(name=f"🤖 {const.bot_prefix}bard <message>", value="Calls Google's LLM -> PaLM 2.", inline=True)
        embed.add_field(name=f"🧮 {const.bot_prefix}latex <message>", value="Calls Google's LLM and asks the model to translate the message into LaTeX code.", inline=True)
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

        #This part initializes the game.
        if message.content == f"{const.bot_prefix}spyfall game":

            embed = discord.Embed(title="Spyfall", description=f"A game of spyfall has been started by {userName}", color=discord.Color.blue())
            embed.add_field(name="How to play?", value="* React 🕵️ to join.\n 1. A location and role will be sent to you in private." 
                            "\n 2. Players take turns asking each other. \n 4. The spy will need to guess your location in order for the spy to win." 
                            "\n 5. $spyfall start", inline=False)
            
            #############
            temporaryembed = await message.channel.send(embed=embed)
            await temporaryembed.add_reaction("🕵️")
            if message.guild in process_dictionary:
                process_dictionary.pop(message.guild)

            process_dictionary[message.guild] = spyFall(message.author.id, message.guild)
            return
        
        if message.content == f"{const.bot_prefix}spyfall start":
            spyfall = process_dictionary[message.guild]
            play : list = spyfall.showplayers()
            await message.channel.send(f"**{client.get_user(spyfall.start())}** is the one asking first.")
            for i in play:
                embed = discord.Embed(title="🕵🏻 SpyFall - Evil Exyrs Bot", description=f"Here is the map and role for \n the SpyFall game at **{message.guild}**.\n", color=discord.Color.red())
                user = client.get_user(i)
                role = spyfall.getrole(i)
                embed.add_field(name=f"MAP:", value=f"```{spyfall.getmap(role)}```", inline=True)
                embed.add_field(name=f"ROLE:", value=f"```{role}```", inline=True)
                embed2 = discord.Embed(title="🕵🏻 SpyFall - Evil Exyrs Bot", description=f"Here is the map and role for \n the SpyFall game at **{message.guild}**.\n", color=discord.Color.red())
                try:
                    await user.send(embed = embed)
                except:
                    embed2.add_field(name=f"Failed to send the private message for {user}", value=f"Please only reveal this map and role if you are {user}", inline=True)
                    embed2.add_field(name=f"MAP:", value=f"||```{spyfall.getmap(role)}```||", inline=False)
                    embed2.add_field(name=f"ROLE:", value=f"||```{role}```||", inline=False)
                    await message.channel.send(embed = embed2)

            return
        
        if message.content == f"{const.bot_prefix}spyfall maps":
            spyfall = process_dictionary[message.guild]
            currentgamemaps = spyfall.maps()
            embed = discord.Embed(title="Spyfall Map Collection", description=f"All maps created in {message.guild}.", color=discord.Color.blue())
            cmaps :str = ""
            for keya in currentgamemaps:
                cmaps = f"{cmaps}* {keya}\n"
            embed.add_field(name="Maps:", value=cmaps, inline=False)
            await message.channel.send(embed=embed)
            return
        
        if message.content == f"{const.bot_prefix}spyfall players":
            spyfall = process_dictionary[message.guild]
            currentplayers = spyfall.showplayers()
            embed = discord.Embed(title="Spyfall players", description=f"All current players in {message.guild}.", color=discord.Color.blue())
            cmaps :str = ""
            for keya in currentplayers:
                cmaps = f"{cmaps}* {client.get_user(keya)}\n"
            embed.add_field(name="Players:", value=cmaps, inline=False)
            await message.channel.send(embed=embed)
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
            array = userMessage.split("rmmap ")[1]
            spyfall = process_dictionary[message.guild]
            await message.channel.send(f"Successfully removed **{array}** containing **{spyfall.removemap(array)}** in maps list.")
            return

        if message.content == f"{const.bot_prefix}spyfall reveal":
            spyfall = process_dictionary[message.guild]
            await message.channel.send(f"The spy is **{client.get_user(spyfall.players[spyfall.spy])}**.")
            spyfall.clearplayers()
            await message.channel.send(f"The spyfall players still ingame after clear is **{spyfall.showplayers()}**.")
            del process_dictionary[message.guild]
            return
        
        if message.content.startswith(f"{const.bot_prefix}spyfall profile new "):
            spyfall = process_dictionary[message.guild]
            nameprof = userMessage.split("profile new ")
            spyfall.newprofile(nameprof[1])
            await message.channel.send(f"{nameprof[1]} profile successfully created.")
            return
        
        if message.content.startswith(f"{const.bot_prefix}spyfall profile change "):
            spyfall = process_dictionary[message.guild]
            try:
                nameprof = userMessage.split("profile change ")
                spyfall.changeprofile(nameprof[1])
                await message.channel.send(f"Successfully switched to {nameprof[1]}.")
            except:
                await message.channel.send(f"Profile does not exist.")
            return

    if message.content == f"{const.bot_prefix}test":
            embed = discord.Embed(title="Test photo", description=f"https://tenor.com/view/baka-anime-gif-22001672", color=discord.Color.blue())
            await message.channel.send(embed = embed)
            await message.channel.send('https://tenor.com/view/baka-anime-gif-22001672')
            return
    
@client.event
async def on_reaction_add(reaction, user):
    constraints: bool =  user != client.user and isinstance(reaction.message.channel, discord.TextChannel)
    constraints = constraints and reaction.message.author == client.user and reaction.emoji == "🕵️"
    if constraints:
        global process_dictionary
        spyfall = process_dictionary[user.guild]
        if not spyfall.addplayer(user.id):
            await reaction.message.channel.send(f"{user.name} is already in the game.")
            return
        else:
            await reaction.message.channel.send(f"{user.name} joined the Spyfall game.")
            return

@client.event
async def on_reaction_remove(reaction, user):
    constraints = user != client.user and isinstance(reaction.message.channel, discord.TextChannel)
    constraints = constraints and reaction.message.author == client.user and reaction.emoji == "🕵️"    
    spyfall = process_dictionary[user.guild]
    if constraints and spyfall.removeplayer(user.id):
        await reaction.message.channel.send(f"{user.name} left the Spyfall game.")
        return

def correctThis(text):
    return TextBlob(text).correct()

client.run(keys.DISCORD_TOKEN)
