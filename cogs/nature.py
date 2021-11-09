import discord
from discord.ext import commands

class Nature(commands.Cog):
    def __init__(self, bot):
        self. bot = bot

    @commands.command()
    async def natures(self, ctx):
        await ctx.send('https://img.rankedboost.com/wp-content/uploads/2016/08/pokemon-go-natures.jpg')

def setup(bot):
    bot.add_cog(Nature(bot))