import discord
from discord.ext import commands
from spyfall import spyFall

class spyfallcog(commands.Cog):
    process_dictionary = {}

    def __init__(self, bot):
        self.process_dictionary = {}
        self.bot = bot
        print("module successfully imported.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game("%help for instructions!"))

    @commands.command()
    async def spy(self, ctx, arg : str):
            if arg == 'game':
                embed = discord.Embed(title="Spyfall", description=f"A game of spyfall has been started by {ctx.author}", color=discord.Color.blue())
                embed.add_field(name="How to play?", value="* React 🕵️ to join.\n 1. A location and role will be sent to you in private." 
                            "\n 2. Players take turns asking each other. \n 4. The spy will need to guess your location in order for the spy to win." 
                            "\n 5. $spyfall start", inline=False)

                temporaryembed = await ctx.channel.send(embed=embed)
                await temporaryembed.add_reaction("🕵️")
                if ctx.guild in self.process_dictionary:
                    self.process_dictionary.pop(ctx.guild)

            self.process_dictionary[ctx.guild] = spyFall(ctx.author.id, ctx.guild)
            return