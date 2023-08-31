import discord
from discord.ext import commands
from .. import const

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("module successfully imported.")

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Evil Exyrs / Help", description="These are the commands available for this bot." 
                              "\n\n **note**: some commands may not work since features can be enabled or disabled.", color=discord.Color.red())
        # embed.add_field(name=f"{const.bot_prefix}math <math equation>", value="Evaluates the mathematical expression, expressions in LaTeX is recommended.", inline=False)
        embed.add_field(name=f"🕵🏻 {const.bot_prefix}spyfall <parameter>", value=f"Starts a game of Spyfall. (**quick start**: {const.bot_prefix}spyfall game)." 
                        "\n\n **🕵🏻 possible parameters**: \"game\", \"start\"," 
                        "\"mkmap <map name> <role1> <role2>...\", \"rmmap <map name>\", \"reveal\""
                        "\n\n**🕵🏻 parameters for map profiles:** \"profile new <profile name>\", \"profile list\", \"profile switch <profile name>\","
                        " \"profile delete <profile name>\"\n\n", inline=False)
        embed.add_field(name=f"🤖 {const.bot_prefix}bard <message>", value="Calls Google's LLM -> PaLM 2.", inline=True)
        embed.add_field(name=f"🧮 {const.bot_prefix}latex <message>", value="Calls Google's LLM and asks the model to translate the message into LaTeX code.", inline=True)
        await ctx.send(embed=embed)
        return