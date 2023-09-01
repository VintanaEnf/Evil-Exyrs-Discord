import discord
from discord.ext import commands
import const
import sys
from help_cog import helpcog
from spyfall_cog import spyfallcog



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


#This will run when the bot begins.
print("The bot is NOW starting, please wait...")
@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))
    await bot.add_cog(helpcog(bot))
    await bot.add_cog(spyfallcog(bot))

#This will log all of the messages in the terminal.
@bot.event
async def on_message(message):
    userName = str(message.author)
    userMessage = str(message.content)
    print(f'{userName} in {message.guild}: {userMessage}')
    await bot.process_commands(message)

# @bot.command()
# async def hello(ctx):
#     await ctx.send("Hello!")
#     return

bot.run(keys.DISCORD_TOKEN)