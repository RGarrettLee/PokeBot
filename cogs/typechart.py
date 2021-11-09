import discord
from discord.ext import commands

class Typechart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['typechart'])
    async def types(self, ctx):
        await ctx.send('https://img.pokemondb.net/images/typechart.png')

def setup(bot):
    bot.add_cog(Typechart(bot))