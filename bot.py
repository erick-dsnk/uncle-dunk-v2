#   Copyright 2020-2022 Tabacaru Eric
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


'''
Uncle Dunk's Bot v2.0
'''
import nextcord
from nextcord.ext import commands
from exts.database import settings_collection

from tokens import TOKEN

def determine_prefix(bot: commands.Bot, message: nextcord.Message):
    if message.guild:
        settings = settings_collection.find_one({"_id": message.guild.id})['settings']

        if 'prefix' in settings.keys():
            return settings['prefix']
        
        else:
            return '-'
    
    else:
        return '-'


intents = nextcord.Intents.all()
client = commands.Bot(command_prefix=determine_prefix, intents=intents)

client.load_extension('exts.apod')
client.load_extension('exts.math')
client.load_extension('exts.entertainment')
client.load_extension('exts.events')
#client.load_extension('exts.games')
client.load_extension('exts.moderation')
client.load_extension('exts.utility')
client.load_extension('exts.economy')
#client.load_extension('exts.settings')
client.load_extension('exts.suggestions')
client.load_extension('exts.managing')
#client.load_extension('exts.music')

@client.command()
async def reauth(ctx: commands.Context):
    if ctx.author.id == 419022467210936330:
        for guild in client.guilds:
            channel = await guild.owner.create_dm()
            embed = nextcord.Embed(
                title=":loud_sound: DISCLAIMER",
                description="Uncle Dunk has been updated to implement Slash Commands, but for this feature to be activated in your server, you will need to reauthorize Uncle Dunk by using the updated invite link on our top.gg page: https://top.gg/bot/743859839821807736",
                color=nextcord.Color.green()
            )

            await channel.send("This is an automated message, and we, at Uncle Dunk development team, are truly sorry for your inconvenience!", embed=embed)

client.run(TOKEN)