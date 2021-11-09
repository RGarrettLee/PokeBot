import discord
import json
import requests
from serpapi import GoogleSearch
from discord.ext import commands

class Item(commands.Cog):
    def loadData(self):
        with open('serverData.json', 'r') as f:
            self.serverData = json.loads(f.read())
            self.emotes = self.serverData['types']

    def __init__(self, bot):
        self.bot = bot
        self.loadData()
        self.link = 'https://pokeapi.co/api/v2/item/'
        self.spellingKey = self.serverData['spellcheck']['token']

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command()
    async def item(self, ctx, *arg):
        message = await ctx.send('Retrieving item...')
        try:
            checkSpelling = self.tupleConvert(arg)

            item = self.tupleConvert(arg)

            item = item.replace(' ', '-')

            if (requests.get(self.link + item).status_code == 200):
                itemData = requests.get(self.link + item).json()

                effect = ''

                for i in itemData['effect_entries']:
                    if (i['language']['name'] == 'en'):
                        effect = i['short_effect']

                embed = discord.Embed(title='{0}'.format(itemData['name'].replace('-', ' ').title()), description='Info about {0}'.format(itemData['name'].replace('-', ' ').title()), color=0xfbca3c)
                embed.set_thumbnail(url=itemData['sprites']['default'])
                embed.add_field(name='**Effect**', value=effect, inline=False)
                if (itemData['fling_effect'] != None):
                    embed.add_field(name='**Fling Effect**', value=itemData['fling_effect']['name'].title(), inline=False)
                embed.add_field(name='**Fling Damage**', value=itemData['fling_power'], inline=False)

                await message.edit(content='Retrieved {0}'.format(itemData['name'].replace('-', ' ').title()), embed=embed)
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
    bot.add_cog(Item(bot))