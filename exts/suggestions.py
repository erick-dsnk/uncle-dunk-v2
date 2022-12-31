import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Context, Bot
from exts.database import settings_collection

class SuggestionModal(nextcord.ui.Modal):
    def __init__(self, bot: commands.Bot, creator: bool):
        super().__init__(
            title="Suggest a Feature!",
            auto_defer=True
        )

        self.bot = bot
        self.creator = creator

        if self.creator is True:
            self.suggestion = nextcord.ui.TextInput(
                label = "Command/Feature",
                placeholder = "Type the command/feature that you would like to see added here...",
                min_length = 1,
                max_length = 1000,
                style = nextcord.TextInputStyle.paragraph
            )
            self.add_item(self.suggestion)

        else:
            self.suggestion = nextcord.ui.TextInput(
                label = "Server Suggestion",
                placeholder = "Type the suggestion you have for this server here...",
                min_length=1,
                max_length=1000,
                style = nextcord.TextInputStyle.paragraph
            )
            self.add_item(self.suggestion)

    async def callback(self, interaction: nextcord.Interaction):
        target = None
        channel = None

        if self.creator is True:
            target = await self.bot.fetch_user(419022467210936330)
            channel = await target.create_dm()

            embed = nextcord.Embed(
                title="Feature Suggestion",
                description=self.suggestion.value,
                color=nextcord.Color.green()
            )
            embed.set_footer(
                text = f"Sent by {interaction.user.name}#{interaction.user.discriminator}.",
                icon_url = interaction.user.avatar.url
            )
            await channel.send(embed=embed)

            return await interaction.response.send_message(":white_check_mark: Sent!", ephemeral=True)

        else:
            target = await self.bot.fetch_user(
                interaction.guild.owner.id
            )
            channel = await target.create_dm()

            embed = nextcord.Embed(
                title="Server Suggestion",
                description=f"""
A suggestion has been sent to you from **{interaction.guild.name}**!\n
```
{self.suggestion.value}
```
"""
            )
            await channel.send(embed=embed)

            return await interaction.response.send_message(":white_check_mark: Sent!", ephemeral=True)



class Suggestions(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot      

    
    @nextcord.slash_command(
        name="feature",
        description="Suggest a new command or feature to the creator of the bot!"
    )
    async def feature(
        self,
        interaction: nextcord.Interaction,
        creator: int = nextcord.SlashOption(
            name="target",
            description="Where you want to send a suggestion (this server or the creator of the bot).",
            choices={"creator": 1, "server": 2},
            required=True
        )
    ):  
        if creator == 1:
            creator = True
        else:
            creator = False

        await interaction.response.send_modal(SuggestionModal(self.bot, creator))



def setup(bot: Bot):
    bot.add_cog(Suggestions(bot))
