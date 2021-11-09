import discord
import json
import requests
import os
from discord.ext import commands

with open('serverData.json', 'r') as f:
    serverData = json.loads(f.read())

token = serverData['bot']['token']

prefix = serverData['prefix']['prefix']

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print(bot.user.name, 'logged in')
    print('-----------------')
    await bot.change_presence(activity=discord.Activity(name='The Elite Four | {0}help'.format(prefix), type=5))

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Help', description='Commands', color=0xfbca3c)
    embed.add_field(name='{0}search / info / pokemon `pokémon`'.format(prefix), value='Search for a pokémon', inline=False)
    embed.add_field(name='{0}location `pokémon`'.format(prefix), value='Find the locations the specified pokémon can be found in', inline=False)
    embed.add_field(name='{0}moveset `pokémon`'.format(prefix), value='Display the moveset of the specified pokémon', inline=False)
    embed.add_field(name='{0}move `move`'.format(prefix), value='Search for a move', inline=False)
    embed.add_field(name='{0}ability `ability`'.format(prefix), value='Search for an ability', inline=False)
    embed.add_field(name='{0}item `item`'.format(prefix), value='Search for an item', inline=False)
    embed.add_field(name='{0}natures'.format(prefix), value='Show the pokémon nature chart', inline=False)
    embed.add_field(name='{0}types / {0}typechart'.format(prefix), value='Shows the type effectiveness chart', inline=False)
    embed.add_field(name='`Created By:`', value='{0}'.format(serverData['author']['id']), inline=False)
    await ctx.send(embed=embed)

for cog in os.listdir("./cogs"):
    if cog.endswith('.py'):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f'{cog} can not be loaded:')
            raise e

bot.run(token)
