import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context, Bot, Cog
from exts.database import settings_collection


class Settings(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setwelcomechannel(self, ctx: Context, channel_id: int):
        '''
        Command to set a designated channel where the bot will send a message when a user joins/leaves the server.
        Requires you to have administrator permission.
        '''

        settings = settings_collection.find_one({"_id": ctx.guild.id})['settings']

        if nextcord.utils.get(ctx.guild.text_channels, id=channel_id):
            settings['welcome_channel'] = channel_id
            settings_collection.find_one_and_update(
                {"_id": ctx.guild.id}, {"$set": {"settings": settings}}
            )

            await ctx.send(":white_check_mark: Successfully set welcome channel!")
        
        else:
            await ctx.send(":x: That's not a valid channel ID!")
        
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setjoinmessage(self, ctx: Context, *, message: str):
        '''
        Set a message that the bot should send when a person joins the server.
        Requires administrator permission.
        You can add `{ mention }` to the message and the bot will replace it with a mention of the user that joined.
        '''

        settings = settings_collection.find_one({"_id": ctx.guild.id})['settings']

        settings['join_message'] = message

        settings_collection.find_one_and_update(
            {"_id": ctx.guild.id},
            {"$set": {"settings": settings}}
        )

        await ctx.send(":white_check_mark: Successfully set join message!")
    

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setleavemessage(self, ctx: Context, *, message: str):
        '''
        Set a message that the bot should send when a person leaves the server.
        Requires administrator permission.
        You can add `{ mention }` to the message and the bot will replace it with a mention of the user that left.
        '''

        settings = settings_collection.find_one({"_id": ctx.guild.id})['settings']

        settings['leave_message'] = message

        settings_collection.find_one_and_update(
            {"_id": ctx.guild.id},
            {"$set": {"settings": settings}}
        )

        await ctx.send(":white_check_mark: Successfully set leave message!")


    @commands.command()
    async def setsuggestionchannel(self, ctx: Context, channel_id: int):
        '''
        Set a channel in which to receive server suggestions.
        '''
        settings = settings_collection.find_one({"_id": ctx.guild.id})['settings']

        if nextcord.utils.get(ctx.guild.text_channels, id=channel_id):
            settings['suggestion_channel'] = channel_id
            settings_collection.find_one_and_update(
                {"_id": ctx.guild.id}, {"$set": {"settings": settings}}
            )

            await ctx.send(":white_check_mark: Successfully set suggestion channel!")
        
        else:
            await ctx.send(":x: That's not a valid channel ID!")


    @commands.has_permissions(administrator=True)
    @commands.command()
    async def prefix(self, ctx: Context, prefix: str = ""):
        if prefix == "":
            settings = settings_collection.find_one({"_id": ctx.guild.id})['settings']

            if 'prefix' in settings.keys():
                embed = nextcord.Embed(
                    title=f":shield: Prefix for **{ctx.guild.name}**",
                    description=f"My prefix: `{settings['prefix']}`",
                    color=nextcord.Color.blurple()
                )

                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")

                await ctx.send(embed=embed)
            
            else:
                embed = nextcord.Embed(
                    title=f":shield: Prefix for **{ctx.guild.name}**",
                    description="My prefix: `-`",
                    color=nextcord.Color.blurple()
                )

                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")

                await ctx.send(embed=embed)

        else:
            settings = settings_collection.find_one({"_id": ctx.guild.id})['settings']

            settings['prefix'] = prefix
            
            settings_collection.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$set": {"settings": settings}}
            )
        
    

def setup(bot):
    bot.add_cog(Settings(bot))
