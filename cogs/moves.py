import discord
import json
import io
import requests
from serpapi import GoogleSearch
from discord.ext import commands

class Moves(commands.Cog):
    def loadData(self):
        with open('serverData.json', 'r') as f:
            self.serverData = json.loads(f.read())
            self.emotes = self.serverData['types']

    def __init__(self, bot):
        self.bot = bot
        self.loadData()
        self.link = 'https://pokeapi.co/api/v2/move/'
        self.hitAll = 'https://i.imgur.com/xlDHKuT.png'
        self.hitDouble = 'https://i.imgur.com/6m0RXfI.png'
        self.hitSingle = 'https://i.imgur.com/X2p0cb2.png'
        self.ally = 'https://i.imgur.com/BZJlsf1.png'
        self.user = 'https://i.imgur.com/GSl79dr.png'
        self.spellingKey = self.serverData['spellcheck']['token']

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command(aliases=['moves'])
    async def move(self, ctx, *arg):
        message = await ctx.send('Retrieving move...')
        try:
            checkSpelling = self.tupleConvert(arg)

            move = self.tupleConvert(arg)
            move = move.replace(' ', '-')


            if (requests.get(self.link + move).status_code == 200):
                moveData = requests.get(self.link + move).json()

                type = '{0} {1}'.format(self.emotes[moveData['type']['name']], self.emotes[moveData['damage_class']['name']])
                effect_chance = moveData['effect_chance']

                embed = discord.Embed(title='{0}'.format(moveData['name'].replace('-', ' ').title()), description='{0}'.format(type), color=0xfbca3c)
                embed.add_field(name='**Effects**', value='{0}'.format(moveData['effect_entries'][0]['short_effect'].replace('$effect_chance', str(effect_chance))), inline=False)
                embed.add_field(name='**Power**', value='{0}'.format(moveData['power']), inline=False)
                embed.add_field(name='**Accuracy**', value='{0}'.format(moveData['accuracy']), inline=False)
                embed.add_field(name='**PP**', value='{0}'.format(moveData['pp']), inline=False)
                embed.add_field(name='**Priority**', value='{0}'.format(moveData['priority']), inline=False)
                if (moveData['target']['name'] == 'all-opponents'): embed.set_image(url=self.hitDouble)
                if (moveData['target']['name'] == 'all-other-pokemon'): embed.set_image(url=self.hitAll)
                if (moveData['target']['name'] == 'selected-pokemon'): embed.set_image(url=self.hitSingle)
                if (moveData['target']['name'] == 'ally'): embed.set_image(url=self.ally)
                if (moveData['target']['name'] == 'user'): embed.set_image(url=self.user)

                await message.edit(content='Retrieved {0}'.format(moveData['name'].replace('-', ' ').title()), embed=embed)
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
    bot.add_cog(Moves(bot))
