import discord
import json
import requests
from serpapi import GoogleSearch
from discord.ext import commands

class Location(commands.Cog):
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

    @commands.command(aliases=['spawn'])
    async def location(self, ctx, *arg):
        message = await ctx.send('Retrieving location info...')
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
                locData = requests.get(pokeData['location_area_encounters']).json()

                locations = ''

                games = {}

                for i in locData:
                    for j in i['version_details']:
                        if (not j['version']['name'].replace('-', ' ').title() in games):
                            games[j['version']['name'].replace('-', ' ').title()] = []
                        games[j['version']['name'].replace('-', ' ').title()].append(i['location_area']['name'].replace('-', ' ').title())

                gameAreas = games.items()

                embed = discord.Embed(title='{0} Encounter Locations'.format(pokeData['name'].format('-', ' ').title()), description='Where to find {0} across the Pokémon games'.format(pokeData['name'].replace('-', ' ').title()), color=0xfbca3c)
                embed.set_thumbnail(url=pokeData['sprites']['other']['home']['front_default'])
                for i in gameAreas:
                    title = i[0]
                    for j in i[1]:
                        locations += j + '\n'
                    embed.add_field(name='**Pokémon {0}**'.format(title), value=locations, inline=False)
                    locations = ''
                await message.edit(content='Retrieved locations', embed=embed)
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
    bot.add_cog(Location(bot))
