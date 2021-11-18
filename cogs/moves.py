import discord
import json
import io
import requests
from fuzzywuzzy import process
from discord.ext import commands

class Moves(commands.Cog):
    def loadData(self):
        with open('serverData.json', 'r') as f:
            self.serverData = json.loads(f.read())
            self.emotes = self.serverData['types']
        data = requests.get(self.link).json()
        limit = data['count']

        self.moves = requests.get(self.count + f'{limit}').json()

        self.names = []

        for i in self.moves['results']:
            self.names.append(i['name'])

    def __init__(self, bot):
        self.bot = bot
        self.link = 'https://pokeapi.co/api/v2/move/'
        self.count = 'https://pokeapi.co/api/v2/move?limit='
        self.hitAll = 'https://i.imgur.com/xlDHKuT.png'
        self.hitDouble = 'https://i.imgur.com/6m0RXfI.png'
        self.hitSingle = 'https://i.imgur.com/X2p0cb2.png'
        self.ally = 'https://i.imgur.com/BZJlsf1.png'
        self.user = 'https://i.imgur.com/GSl79dr.png'
        self.loadData()

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command(aliases=['moves'])
    async def move(self, ctx, *arg):
        message = await ctx.send('Retrieving move...')
        try:
            move = self.tupleConvert(arg)
            move = move.replace(' ', '-')

            highest = process.extractOne(move, self.names)
            newMove = highest[0].replace(' ', '-').replace('.', '').replace("'", '')

            if (requests.get(self.link + newMove).status_code == 200):
                moveData = requests.get(self.link + newMove).json()

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
        except:
            await message.edit(content='An error occured')



def setup(bot):
    bot.add_cog(Moves(bot))