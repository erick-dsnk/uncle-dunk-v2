import nextcord
from nextcord import Game
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Context, Bot
from nextcord.ext.commands.errors import CommandNotFound
from nextcord.utils import get
from exts.database import economy_collection, settings_collection


def setup_database(client: Bot):
    for guild in client.guilds:
        if not economy_collection.find_one({"_id": guild.id}):
            members = []

            for member in guild.members:
                members.append(
                    {"id": member.id, "money": 0, "bank": 0}
                )

            economy_collection.insert_one(
                {
                    "_id": guild.id,
                    "name": guild.name,
                    "members": members
                }
            )
        
        else:
            pass
        

        if not settings_collection.find_one({"_id": guild.id}):
            settings_collection.insert_one(
                {
                    "_id": guild.id,
                    "name": guild.name,
                    "settings": {}
                }
            )
        
        else:
            pass
        


class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    

    @Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=nextcord.Status.online, activity=Game(name="-help to see a list of commands!"))
        setup_database(self.bot)
        
        print('Uncle Dunk\'s bot is in the house and he ain\'t leaving')

    
    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(f':x: That\'s not a command!')
        
        else:
            print(error)
    

    @Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        members_data = economy_collection.find_one({"_id": member.guild.id})['members']

        members_data.append({"id": member.id, "money": 0, "bank": 0})

        economy_collection.find_one_and_update({"_id": member.guild.id}, {"$set": {"members": members_data}})


        settings = settings_collection.find_one({"_id": member.guild.id})['settings']

        if 'welcome_channel' in settings.keys():
            welcome_channel = get(member.guild.text_channels, id=settings['welcome_channel'])

            if 'join_message' in settings.keys():
                join_message = settings['join_message']

                if "{ mention }" in join_message:
                    join_message.replace("{ mention }", member.mention)

                embed = nextcord.Embed(
                    title=f"**{member.guild.name}**",
                    description=f"{join_message}",
                    color=nextcord.Color.green()
                )

                await welcome_channel.send(embed=embed)
            
            else:
                embed = nextcord.Embed(
                    title=f"**{member.guild.name}**",
                    description=f"Welcome to {member.guild.name}! :partying_face:",
                    color=nextcord.Color.green()
                )

                await welcome_channel.send(embed=embed)
        
        else:
            pass


    @Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        members_data = economy_collection.find_one({"_id": member.guild.id})['members']

        i = 0

        for user in members_data:
            if user['id'] == member.id:
                del members_data[i]
                break
            
            else:
                pass

            i += 1
        
        economy_collection.find_one_and_update({"_id": member.guild.id}, {"$set": {"members": members_data}})


        settings = settings_collection.find_one({"_id": member.guild.id})['settings']

        if 'welcome_channel' in settings.keys():
            welcome_channel = get(member.guild.text_channels, id=settings['welcome_channel'])

            if 'leave_message' in settings.keys():
                leave_message = settings['leave_message']

                if "{ mention }" in leave_message:
                    leave_message.replace("{ mention }", member.mention)

                embed = nextcord.Embed(
                    title=f"**{member.guild.name}**",
                    description=f"{leave_message}",
                    color=nextcord.Color.dark_purple()
                )

                await welcome_channel.send(embed=embed)
            
            else:
                embed = nextcord.Embed(
                    title=f"**{member.guild.name}**",
                    description=f"Bye {member.mention}! We're sorry to see you go :(",
                    color=nextcord.Color.dark_purple()
                )

                await welcome_channel.send(embed=embed)
        
        else:
            pass


    @Cog.listener()
    async def on_guild_join(self, guild):
        setup_database(self.bot)
    
    @Cog.listener()
    async def on_guild_remove(self, guild):
        economy_collection.delete_one({"_id": guild.id})
        settings_collection.delete_one({"_id": guild.id})


def setup(bot):
    bot.add_cog(Events(bot))
