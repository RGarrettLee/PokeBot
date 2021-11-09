import discord
import json
import requests
from serpapi import GoogleSearch
from discord.ext import commands

class Moveset(commands.Cog):
    def loadData(self):
        with open('serverData.json', 'r') as f:
            self.serverData = json.loads(f.read())
            self.emotes = self.serverData['types']

    def __init__(self, bot):
        self.bot = bot
        self.loadData()
        self.link = 'https://pokeapi.co/api/v2/pokemon/'
        self.spellingKey = self.serverData['spellcheck']['token']

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command()
    async def moveset(self, ctx, *arg):
        message = await ctx.send('Retrieving moveset...')
        try:
            checkSpelling = self.tupleConvert(arg)
            if (arg[0].lower() == 'alolan' or arg[0] == 'galarian' or arg[0] == 'mega' or arg[0] == 'gigantamax' or arg[0] == 'gmax' or arg[0] == 'primal'):
                form = arg[::-1]
                pokemon = self.tupleConvert(form)
                pokemon = pokemon.replace('alolan', 'alola').replace('galarian', 'galar').replace('gigantamax', 'gmax')
            else:
                pokemon = self.tupleConvert(arg)

            pokemon = pokemon.replace(' ', '-').replace('.', '').replace("'", '')

            if (requests.get(self.link + pokemon).status_code == 200):
                pokeData = requests.get(self.link + pokemon).json()

                moves = ''
                for i in pokeData['moves']:
                    moves += i['move']['name'].replace('-', ' ').title() + '\n'

                embed = discord.Embed(title='Moves learned by {0}'.format(pokeData['name'].replace('-', ' ').title()), description='', color=0xfbca3c)
                embed.set_thumbnail(url=pokeData['sprites']['other']['home']['front_default'])
                embed.add_field(name='**Learnset**', value=moves, inline=False)

                await message.edit(content="Retrieved {0}'s moveset".format(pokeData['name'].replace('-', ' ').title()), embed=embed)
            else:
                params = {
                    "q": checkSpelling,
                    "hl": "en",
                    "gl": "us",
                    "api_key": self.spellingKey
                }
                search = GoogleSearch(params)
                results = search.get_dict()
                search_information = results['search_information']
                fixedSpelling = search_information['showing_results_for']
                await message.edit(content=f'{checkSpelling} could not be found. Did you mean {fixedSpelling}?')
        except:
            await message.edit(content='An error occured')

def setup(bot):
    bot.add_cog(Moveset(bot))