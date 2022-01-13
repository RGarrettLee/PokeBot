import discord
import json
import requests
import io
from fuzzywuzzy import process
from discord.ext import commands

class Search(commands.Cog):
    def loadData(self):
        with open('serverData.json', 'r') as f:
            self.serverData = json.loads(f.read())
            self.emotes = self.serverData['types']
        data = requests.get(self.link).json()
        limit = data['count']

        pokemon = requests.get(self.count + f'{limit}').json()

        self.names = []

        for i in pokemon['results']:
            self.names.append(i['name'])

    def __init__(self, bot):
        self.bot = bot
        self.link = 'https://pokeapi.co/api/v2/pokemon/'
        self.count = 'https://pokeapi.co/api/v2/pokemon?limit='
        self.loadData()

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command(aliases=['pokemon', 'info', 'pokémon'])
    async def search(self, ctx, *arg):
        message = await ctx.send('Retrieving Pokémon...')
        try:
            if (arg[0].lower() == 'alolan' or arg[0] == 'galarian' or arg[0] == 'mega' or arg[0] == 'gigantamax' or arg[0] == 'gigantimax' or arg[0] == 'gmax' or arg[0] == 'primal'):
                form = arg[::-1]
                pokemon = self.tupleConvert(form)
                pokemon = pokemon.replace('alolan', 'alola').replace('galarian', 'galar').replace('gigantamax', 'gmax').replace('gigantimax', 'gmax')
            else:
                pokemon = self.tupleConvert(arg)

            pokemon = pokemon.replace(' ', '-').replace('.', '').replace("'", '')

            highest = process.extractOne(pokemon, self.names)
            newPoke = highest[0].replace(' ', '-').replace('.', '').replace("'", '')

            if (requests.get(self.link + newPoke).status_code == 200):
                pokeData = requests.get(self.link + newPoke).json()
                extraData = requests.get(pokeData['species']['url']).json()
                evoData = requests.get(extraData['evolution_chain']['url']).json()
                abilities = ''

                for i in pokeData['abilities']:
                    if (i['is_hidden']):
                        abilities += '__*Hidden Ability:*__ {0}'.format(i['ability']['name'].replace('-', ' ').title())
                    else:
                        abilities += '{0}\n'.format(i['ability']['name'].replace('-', ' ').title())

                eggGroups = ''

                try:
                    for i in extraData['egg_groups']:
                        eggGroups += i['name'].title() + '\n'
                except:
                    pass

                type = ''

                for i in pokeData['types']:
                    type += self.emotes[i['type']['name']] + ' '

                flavourText = ''

                for i in extraData['flavor_text_entries']:
                    if (i['language']['name'] == 'en'):
                        flavourText = i['flavor_text'].replace('\n', ' ').strip()
                        break

                evolved = ''
                evolves = ''

                try:
                    if (pokemon == evoData['chain']['species']['name']):
                        evolves = evoData['chain']['evolves_to'][0]['species']['name'].title()
                    if (pokemon == evoData['chain']['evolves_to'][0]['species']['name']):
                        evolved = evoData['chain']['species']['name'].title()
                        evolves = evoData['chain']['evolves_to'][0]['evolves_to'][0]['species']['name'].title()
                    if (pokemon == evoData['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']):
                        evolved = evoData['chain']['evolves_to'][0]['species']['name'].title()
                except:
                    pass

                bst = pokeData['stats'][0]['base_stat'] + pokeData['stats'][1]['base_stat'] + pokeData['stats'][2]['base_stat'] + pokeData['stats'][3]['base_stat'] + pokeData['stats'][4]['base_stat'] + pokeData['stats'][5]['base_stat']
                embed = discord.Embed(title='{0}'.format(pokeData['name'].replace('-', ' ').title()), description='{0}'.format(type), color=0xfbca3c)
                embed.set_image(url=pokeData['sprites']['other']['home']['front_default'])
                embed.set_author(name='Pokédex #{0}'.format(pokeData['id']))
                embed.set_footer(text='{0}'.format(flavourText))
                embed.add_field(name='**Abilities**', value=f'{abilities}', inline=False)
                embed.add_field(name='**Base Stats**', value='**HP**: {0} \n **Attack**: {1} \n **Defense**: {2} \n **Sp. Atk**: {3} \n **Sp. Def**: {4} \n **Speed**: {5} \n **Base Stat Total**: {6}'.format(pokeData['stats'][0]['base_stat'], pokeData['stats'][1]['base_stat'], pokeData['stats'][2]['base_stat'], pokeData['stats'][3]['base_stat'], pokeData['stats'][4]['base_stat'], pokeData['stats'][5]['base_stat'], bst), inline=False)
                if (eggGroups == ''):
                    embed.add_field(name='**Egg Groups**', value='Undefined', inline=True)
                else:
                    embed.add_field(name='**Egg Groups**', value=eggGroups, inline=True)
                embed.add_field(name='**Steps to Hatch**', value=int(extraData['hatch_counter']) * 257, inline=True)
                embed.add_field(name='**Catch Rate**', value=extraData['capture_rate'], inline=True)
                if (evolved != ''): embed.add_field(name='**Previous Evolution**', value=evolved, inline=True)
                if (evolves != ''): embed.add_field(name='**Next Evolution**', value=evolves, inline=True)

                await message.edit(content='Retrieved {0}'.format(pokeData['name'].replace('-', ' ').title()), embed=embed)
        except:
            await message.edit(content='Specify a form if the pokémon has multiple (ex. deoxys -> depxys normal)')

def setup(bot):
    bot.add_cog(Search(bot))