import nextcord
from nextcord.ext import commands, application_checks
from nextcord.ext.commands import Bot, Cog, MissingPermissions

class Manager(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @nextcord.slash_command(
        name="announce",
        description="Make an announcement with a fancy embed containing your important message."
    )
    @application_checks.has_permissions(kick_members=True)
    async def announce(
        self,
        interaction: nextcord.Interaction,
        channel: str = nextcord.SlashOption(
            name="channel",
            description="The channel you want to send your announcement in.",
            required=True
        ),
        message: str = nextcord.SlashOption(
            name="message",
            description="The message you want to announce.",
            required=True
        ),
        mention: int = nextcord.SlashOption(
            name="mention",
            description="Mention everyone or don't mention. Defaults to no mention.",
            required=False,
            default="",
            choices={
                "no mention": 1,
                "everyone": 2
            }
        )
    ):
        desc = f"{message}"
        allowed_mentions = nextcord.AllowedMentions(everyone=True)

        if mention == 2:
            desc += "\n@everyone"

        embed = nextcord.Embed(
            title=":loudspeaker: **Important announcement!**",
            description=desc,
            color=nextcord.Color.green()
        )

        embed.set_footer(text=f"Announcement made by {interaction.user.name}#{interaction.user.discriminator}.")

        await channel.send(embed=embed, allowed_mentions=allowed_mentions)

    @announce.error
    async def announce_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, MissingPermissions):
            embed = nextcord.Embed(
                name="Missing Permissions!",
                description="You don't have the required persmissions to use this command!",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
    
def setup(bot: Bot):
    bot.add_cog(Manager(Bot))