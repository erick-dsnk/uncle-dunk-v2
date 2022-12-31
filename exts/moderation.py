import datetime
import nextcord
from nextcord.ext import commands, application_checks
from nextcord.ext.commands import MissingPermissions
import humanfriendly

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="kick",
        description="Kick a member from the server."
    )
    @application_checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            name="member",
            description="The member you want to kick.",
            required=True
        ),
        reason: str = nextcord.SlashOption(
            name="reason",
            description="Reason for kick.",
            required=False,
            default="None specified."
        )
    ):        
        await interaction.response.defer(ephemeral=True)

        dm_channel = member.create_dm()

        embed = nextcord.Embed(
            title=f'You have been kicked from {interaction.guild.name}!',
            description=f"**Staff Member:** `{interaction.user.name}#{interaction.user.discriminator}`\n**Reason**: `{reason}`",
            color=nextcord.Color.red()
        )

        await member.kick(reason=reason)

        await interaction.followup.send(f":white_check_mark: Kicked user {member.name}#{member.discriminator} for reason: {reason}.")
        await dm_channel.send(embed=embed)

    @kick.error
    async def kick_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, MissingPermissions):
            embed = nextcord.Embed(
                title=f'Missing Permissions!',
                description=f':x: You don\'t have the required permissions to use this command!',
                color=nextcord.Color.red()
            )
            await interaction.response.send(embed=embed)

    @nextcord.slash_command(
        name="ban",
        description="Ban a member from the server."
    )
    @application_checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            name="member",
            description="The member you want to ban.",
            required=True
        ),
        reason: str = nextcord.SlashOption(
            name="reason",
            description="Reason for ban.",
            required=False,
            default="None specified."
        )
    ):
        await interaction.response.defer(ephemeral=True)
        dm_channel = await member.create_dm()

        embed = nextcord.Embed(
            title=f'You have been banned from {interaction.guild.name}!',
            description=f"**Staff Member:** `{interaction.user.name}#{interaction.user.discriminator}`\n**Reason**: `{reason}`",
            color=nextcord.Color.red()
        )

        await member.ban(reason=reason)

        await interaction.followup.send(f":white_check_mark: Banned user {member.name}#{member.discriminator} for reason: {reason}.")
        await dm_channel.send(embed=embed)
    
    @ban.error
    async def ban_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, MissingPermissions):
            embed = nextcord.Embed(
                title=f'Missing Permissions!',
                description=f':x: You don\'t have the required permissions to use this command!',
                color=nextcord.Color.red()
            )
            await interaction.response.send(embed=embed)


    @nextcord.slash_command(
        name="mute",
        description="Restrict a member from sending messages."
    )
    @application_checks.has_permissions(kick_members=True)
    async def mute(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The member you want to mute.",
            required=True
        ),
        duration: str = nextcord.SlashOption(
            name="duration",
            description="For how long you want to mute the member. Defaults to 15m.",
            required=False,
            default="15m"
        )
    ):
        embed = nextcord.Embed(
            title=":zipper_mouth: Shush!",
            description=f"User {user.mention} has been muted for `{duration}`.",
            color=nextcord.Color.green()
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

        duration = humanfriendly.parse_timespan(duration)
        await user.edit(timeout=(nextcord.utils.utcnow() + datetime.timedelta(duration)))

        await interaction.response.send_message(embed=embed)

    @mute.error
    async def mute_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, MissingPermissions):
            embed = nextcord.Embed(
                title=f'Missing Permissions!',
                description=f':x: You don\'t have the required permissions to use this command!',
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="unmute",
        description="Gives a member ability to send messages again."
    )
    @application_checks.has_permissions(kick_members=True)
    async def unmute(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The user you want to unmute.",
            required=True
        )
    ):
        embed = nextcord.Embed(
            title="Un-shush!",
            description=f"User {user.mention} has been unmuted!",
            color=nextcord.Color.green()
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        await user.edit(timeout=None)
        
        await interaction.response.send_message(embed=embed)

    @unmute.error
    async def unmute_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, MissingPermissions):
            embed = nextcord.Embed(
                title=f'Missing Permissions!',
                description=f':x: You don\'t have the required permissions to use this command!',
                color=nextcord.Color.red()
            )
            await interaction.response.send(embed=embed)

    @nextcord.slash_command(
        name="silence",
        description="Mutes everyone in the channel."
    )
    async def silence(
        self,
        interaction: nextcord.Interaction,
        duration: str = nextcord.SlashOption(
            name="duration",
            description="For how long you want to mute this channel. Defaults to 15m.",
            required=False,
            default="15m"
        )
    ):
        embed = nextcord.Embed(
            name=":zipper_mouth: Silence in court!",
            description=f"Muted the channel for {duration}",
            color=nextcord.Color.green()
        )

        duration = humanfriendly.parse_timespan(duration)

        for member in interaction.channel.members:
            await member.edit(timeout=(nextcord.utils.utcnow() + datetime.timedelta(duration)))

        await interaction.response.send_message(embed=embed)

    @silence.error
    async def silence_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                title=f'Missing Permissions!',
                description=f':x: You don\'t have the required permissions to use this command!',
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="unsilence",
        description="Give back members of the channel the permission to chat again."
    )
    @application_checks.has_permissions(kick_members=True)
    async def unsilence(
        self,
        interaction: nextcord.Interaction
    ):
        embed = nextcord.Embed(
            name="Okay... no more silence in court.",
            description="Unmuted the channel.",
            color=nextcord.Color.green()
        )

        for member in interaction.channel.members:
            await member.edit(timeout=None)

        await interaction.response.send_message(embed=embed)

    @unsilence.error
    async def unsilence_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                title=f'Missing Permissions!',
                description=f':x: You don\'t have the required permissions to use this command!',
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        

    @nextcord.slash_command(
        name="purge",
        description="Clear an amount of messages."
    )
    @application_checks.has_permissions(manage_messages=True)
    async def purge(
        self,
        interaction: nextcord.Interaction,
        amount: int = nextcord.SlashOption(
            name="amount",
            description="How many messages you want to delete. Defaults to 100.",
            required=False,
            default=100
        )
    ):  
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=amount)

        await interaction.response.send_message(f":white_check_mark: Successfully cleared {amount} messages!", ephemeral=True)

    @purge.error
    async def purge_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, MissingPermissions):
            embed = nextcord.Embed(
                title=f'Missing Permissions!',
                description=f':x: You don\'t have the required permissions to use this command!',
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
