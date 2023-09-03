import discord
from discord.ext import commands
from spyfall import spyFall
import asyncio

class spyfallcog(commands.Cog):
    process_dictionary = {}
    def __init__(self, bot):
        self.process_dictionary = {}
        self.bot = bot
        print("spyfall cog successfully imported.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game("%help for instructions!"))

    @commands.command()
    async def spy(self, ctx, arg : str):
        if arg == 'innit':
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
    
        if arg == 'start':
            spyfall = self.process_dictionary[ctx.guild]
            play : list = spyfall.showplayers()
            await ctx.send(f"**{self.bot.get_user(spyfall.start())}** is the one asking first.")
            for i in play:
                embed = discord.Embed(title="🕵🏻 SpyFall - Evil Exyrs Bot", description=f"Here is the map and role for \n the SpyFall game at **{ctx.guild}**.\n", color=discord.Color.red())
                user = self.bot.get_user(i)
                role = spyfall.getrole(i)
                embed.add_field(name=f"MAP:", value=f"```{spyfall.getmap(role)}```", inline=True)
                embed.add_field(name=f"ROLE:", value=f"```{role}```", inline=True)
                embed2 = discord.Embed(title="🕵🏻 SpyFall - Evil Exyrs Bot", description=f"Here is the map and role for \n the SpyFall game at **{ctx.guild}**.\n", color=discord.Color.red())
                try:
                    await user.send(embed = embed)
                except:
                    embed2.add_field(name=f"Failed to send the private message for {user}", value=f"Please only reveal this map and role if you are {user}", inline=True)
                    embed2.add_field(name=f"MAP:", value=f"||```{spyfall.getmap(role)}```||", inline=False)
                    embed2.add_field(name=f"ROLE:", value=f"||```{role}```||", inline=False)
                    await ctx.channel.send(embed = embed2)
            await ctx.channel.send("The 5 minutes timer starts now.")
            await asyncio.sleep(60*5)
            try:
                if self.process_dictionary[ctx.guild] != None:
                    await ctx.channel.send("Your time of 5 minutes is now finished, guess who the spy is.")
                    await ctx.channel.send("**%spy reveal** to reveal the spy.")
            except:
                    print("spyfall ended already.")
            return
        
        if arg == 'maps':
            spyfall = self.process_dictionary[ctx.guild]
            currentgamemaps = spyfall.maps()
            embed = discord.Embed(title="Current Maps List / SpyFall", description=f"Maps list created in {ctx.guild}.", color=discord.Color.blue())
            cmaps :str = ""
            for keya in currentgamemaps:
                cmaps = f"{cmaps}* {keya}\n"
            embed.add_field(name="Maps:", value=cmaps, inline=False)
            await ctx.channel.send(embed=embed)
            return
            
        if arg == 'players':
            spyfall = self.process_dictionary[ctx.guild]
            currentplayers = spyfall.showplayers()
            embed = discord.Embed(title="Spyfall players", description=f"All current players in {ctx.guild}.", color=discord.Color.blue())
            cmaps :str = ""
            for keya in currentplayers:
                cmaps = f"{cmaps}* {self.bot.get_user(keya)}\n"
            embed.add_field(name="Players:", value=cmaps, inline=False)
            await ctx.channel.send(embed=embed)
            return
        
        if arg == 'mkmap':
            print(ctx.message.content)
            messageonly = ctx.message.content.split("mkmap ")[1]
            listtemp : list = []
            spyfall = self.process_dictionary[ctx.guild]
            t = messageonly.split(", ")
            for i in t:
                listtemp.append(i)
            listtemp.append("spy")
            mapname = listtemp[0]
            listtemp.remove(listtemp[0])
            spyfall.addmap(mapname, listtemp)
            await ctx.channel.send(f"Successfully added **{mapname}** containing **{listtemp}** in maps list.")
            return
        
        if arg == 'rmmap':
            array = ctx.message.content.split("rmmap ")[1]
            spyfall = self.process_dictionary[ctx.guild]
            await ctx.channel.send(f"Successfully removed **{array}** containing **{spyfall.removemap(array)}** in maps list.")
            return
        
        if arg == 'reveal':
            spyfall = self.process_dictionary[ctx.guild]
            await ctx.channel.send(f"The spy is **{self.bot.get_user(spyfall.players[spyfall.spy])}**.")
            spyfall.clearplayers()
            self.process_dictionary.pop(ctx.guild)
            return
        
        if arg == 'pfnew':
            spyfall = self.process_dictionary[ctx.guild]
            nameprof = ctx.message.content.split("pfnew ")
            spyfall.newprofile(nameprof[1])
            await ctx.channel.send(f"{nameprof[1]} profile successfully created.")
            return
        
        if arg == 'pfswitch':
            spyfall = self.process_dictionary[ctx.guild]
            try:
                nameprof = ctx.message.content.split("pfswitch ")
                spyfall.changeprofile(nameprof[1])
                await ctx.channel.send(f"Successfully switched to {nameprof[1]}.")
            except:
                await ctx.channel.send(f"Profile does not exist.")
            return
        
        if arg == 'pflist':
            spyfall = self.process_dictionary[ctx.guild]
            profile_list = spyfall.showprofile()
            embed = discord.Embed(title="Profiles List / SpyFall", description=f"Here are the profiles for the server {ctx.guild}.", color=discord.Color.blue())
            a : str = ""
            for i in profile_list:
                a = f"{a}\n{i}"
            embed.add_field(name="Profiles:", value=a, inline=False)
            await ctx.channel.send(embed = embed)
            return
        
        if arg == 'pfdel':
            spyfall = self.process_dictionary[ctx.guild]
            try:
                nameprof = ctx.message.content.split("profile delete ")
                spyfall.deleteprofile(nameprof[1])
                await ctx.channel.send(f"Successfully deleted profile: {nameprof[1]}.")
            except:
                await ctx.channel.send(f"Profile does not exist.")
            return
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        constraints: bool =  user != self.bot.user and isinstance(reaction.message.channel, discord.TextChannel)
        constraints = constraints and reaction.message.author == self.bot.user and reaction.emoji == "🕵️"
        if constraints:
            spyfall = self.process_dictionary[user.guild]
            if not spyfall.addplayer(user.id):
                await reaction.message.channel.send(f"{user.name} is already in the game.")
                return
            else:
                await reaction.message.channel.send(f"{user.name} joined the Spyfall game.")
                return

    @commands.Cog.listener()    
    async def on_reaction_remove(self, reaction, user):
        constraints = user != self.bot.user and isinstance(reaction.message.channel, discord.TextChannel)
        constraints = constraints and reaction.message.author == self.bot.user and reaction.emoji == "🕵️"    
        spyfall = self.process_dictionary[user.guild]
        if constraints and spyfall.removeplayer(user.id):
            await reaction.message.channel.send(f"{user.name} left the Spyfall game.")
            return