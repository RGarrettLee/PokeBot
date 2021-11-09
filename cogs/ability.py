import discord
import json
import requests
from serpapi import GoogleSearch
from discord.ext import commands

class Ability(commands.Cog):
    def loadData(self):
        with open('serverData.json', 'r') as f:
            self.serverData = json.loads(f.read())
            self.emotes = self.serverData['types']

    def __init__(self, bot):
        self.bot = bot
        self.loadData()
        self.link = 'https://pokeapi.co/api/v2/ability/'
        self.spellingKey = self.serverData['spellcheck']['token']

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command()
    async def ability(self, ctx, *arg):
        message = await ctx.send('Retrieving ability...')
        try:
            checkSpelling = self.tupleConvert(arg)
            ability = self.tupleConvert(arg)

            ability = ability.replace(' ', '-')

            if (requests.get(self.link + ability).status_code == 200):
                abilityData = requests.get(self.link + ability).json()

                effect = ''
                for i in abilityData['effect_entries']:
                    if (i['language']['name'] == 'en'):
                        effect = i['short_effect']

                pokemon = ''

                for i in abilityData['pokemon']:
                    pokemon += i['pokemon']['name'].replace('-', ' ').title() + '\n'

                embed = discord.Embed(title='{0}'.format(abilityData['name'].replace('-', ' ').title()), description='What {0} does, when it was introduced, and what pokémon get it'.format(abilityData['name'].replace('-', ' ').title()), color=0xfbca3c)
                embed.add_field(name='**Effect**', value=effect, inline=False)
                embed.add_field(name='**Introduced in**', value='Generation {0}'.format(abilityData['generation']['name'].replace('generation-', '').upper()), inline=False)
                embed.add_field(name='**Pokémon that get {0}**'.format(abilityData['name'].replace('-', ' ').title()), value=pokemon, inline=False)

                await message.edit(content='Retrieved {0}'.format(abilityData['name'].replace('-', ' ').title()), embed=embed)
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
    bot.add_cog(Ability(bot))