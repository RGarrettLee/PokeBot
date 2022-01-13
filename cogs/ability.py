import discord
import json
import requests
from fuzzywuzzy import process
from discord.ext import commands

class Ability(commands.Cog):
    def loadData(self):
        with open('serverData.json', 'r') as f:
            self.serverData = json.loads(f.read())
            self.emotes = self.serverData['types']
        data = requests.get(self.link).json()
        limit = data['count']

        abilities = requests.get(self.count + f'{limit}').json()

        self.names = []

        for i in abilities['results']:
            self.names.append(i['name'])

    def __init__(self, bot):
        self.bot = bot
        self.link = 'https://pokeapi.co/api/v2/ability/'
        self.count = 'https://pokeapi.co/api/v2/ability?limit='
        self.loadData()

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command()
    async def ability(self, ctx, *arg):
        message = await ctx.send('Retrieving ability...')
        try:
            ability = self.tupleConvert(arg)

            ability = ability.replace(' ', '-')

            highest = process.extractOne(ability, self.names)
            newAbility = highest[0].replace(' ', '-').replace('.', '').replace("'", '')

            if (requests.get(self.link + newAbility).status_code == 200):
                abilityData = requests.get(self.link + newAbility).json()

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
        except:
            await message.edit(content='An error occured')


def setup(bot):
    bot.add_cog(Ability(bot))