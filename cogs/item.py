import discord
import json
import requests
from fuzzywuzzy import process
from discord.ext import commands

class Item(commands.Cog):
    def loadData(self):
        with open('serverData.json', 'r') as f:
            self.serverData = json.loads(f.read())
            self.emotes = self.serverData['types']
        data = requests.get(self.link).json()
        limit = data['count']

        self.items = requests.get(self.count + f'{limit}').json()

        self.names = []

        for i in self.items['results']:
            self.names.append(i['name'])

    def __init__(self, bot):
        self.bot = bot
        self.link = 'https://pokeapi.co/api/v2/item/'
        self.count = 'https://pokeapi.co/api/v2/item?limit='
        self.loadData()

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command()
    async def item(self, ctx, *arg):
        message = await ctx.send('Retrieving item...')
        try:
            item = self.tupleConvert(arg)

            item = item.replace(' ', '-')

            highest = process.extractOne(item, self.names)
            newItem = highest[0].replace(' ', '-')

            if (requests.get(self.link + newItem).status_code == 200):
                itemData = requests.get(self.link + newItem).json()

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
        except:
            await message.edit(content='An error occured')


def setup(bot):
    bot.add_cog(Item(bot))