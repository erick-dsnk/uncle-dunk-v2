import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Context, Bot
from exts.database import economy_collection
import random


def convert_to_time(seconds):
    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return f"{hours} hours, {minutes} minutes, {seconds} seconds"


class Economy(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @nextcord.slash_command(
        name="work",
        description="Earn your money the honest way!"
    )
    async def work(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        guild_data = economy_collection.find_one({"_id": interaction.guild.id})

        members_data = guild_data['members']

        for member in members_data:
            if member['id'] == interaction.user.id:
                amount = random.randint(50, 300)
                member['money'] += amount

                break
            
            else:
                pass
        
        economy_collection.find_one_and_update({"_id": interaction.guild.id}, {"$set": {"members": members_data}})
        
        embed = nextcord.Embed(
            title=":office: Job",
            description=f"You earned `{amount}` Dunk Dollars!",
            color=nextcord.Color.brand_green()
        )

        await interaction.followup.send(embed=embed)
    
    @work.error
    async def work_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You're on cooldown! You will be able to use that command in **{convert_to_time(error.retry_after)}**!")


    @nextcord.slash_command(
        name="rob",
        description="Robbing, high risk, high reward!"
    )
    async def rob(
        self,
        interaction: nextcord.Interaction,
        target: nextcord.Member = nextcord.SlashOption(
            name="target",
            description="The person you want to rob.",
            required=True
        )
    ):
        await interaction.response.defer()
        
        members_data = economy_collection.find_one({"_id": interaction.guild.id})['members']

        robber = interaction.user
        victim = target

        success = random.random() * 100

        amount = random.randint(300, 1000)
        fine = random.randint(100, 200)

        if success >= 30.0:
            for member in members_data:
                if member['id'] == robber.id:
                    if member['money'] < fine:
                        member['money'] = 0
                    
                    else:
                        member['money'] -= fine
                
                elif member['id'] == victim.id:
                    member['money'] += fine * 2
                
                else:
                    pass
            
            embed = nextcord.Embed(
                title="Busted!",
                description=f"You tried robbing {victim.mention} but you got caught and you lost `{amount}` Dunk Dollars!",
                color=nextcord.Color.red()
            )

            await interaction.followup.send(embed=embed)

                
        else:
            for member in members_data:
                if member['id'] == robber.id:
                    member['money'] += amount

                elif member['id'] == victim.id:
                    if member['money'] < (amount / 2):
                        member['money'] = 0
                    
                    else:
                        member['money'] -= (amount / 2)
                else:
                    pass
            
            embed = nextcord.Embed(
                title="Success!",
                description=f"You managed to get away with robbing {victim.mention} and earned `{amount}` Dunk Dollars!",
                color=nextcord.Color.green()
            )

            await interaction.followup.send(embed=embed)
                
        economy_collection.update_one({"_id": interaction.guild.id}, {"$set": {"members": members_data}})

    @rob.error
    async def rob_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You're on cooldown! You will be able to use that command in **{convert_to_time(error.retry_after)}**!")


    @nextcord.slash_command(
        name="daily",
        description="Collect your daily 500 Dunk Dollar bonus!"
    )
    async def daily(self, interaction: nextcord.Interaction):
        await interaction.response.defer()

        members = economy_collection.find_one({"_id": interaction.guild.id})['members']

        for member in members:
            if member['id'] == interaction.user.id:
                member['money'] += 500
        
        embed = nextcord.Embed(
            title="**Daily bonus!**",
            description=":white_check_mark: Successfully claimed your daily `500` dunk dollars bonus!",
            color=nextcord.Color.green()
        )

        economy_collection.find_one_and_update({"_id": interaction.guild.id}, {"$set": {"members": members}})

        await interaction.followup.send(embed=embed)


    @daily.error
    async def daily_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You're on cooldown! You will be able to use that command in **{convert_to_time(error.retry_after)}**!")


    @nextcord.slash_command(
        name="balance",
        description="Check an account's balance."
    )
    async def balance(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The user whose account balance you want to check.",
            required=False,
            default=None
        )
    ):
        await interaction.response.defer()

        if user == None:
            user = interaction.user
        
        members_data = economy_collection.find_one({"_id": interaction.guild.id})['members']

        for member in members_data:
            if member['id'] == user.id:
                embed = nextcord.Embed(
                    title=":bank: Bank of Dunkville",
                    description=f"Bank statement of {user.name}#{user.discriminator}",
                    color=nextcord.Color.green()
                )

                embed.add_field(
                    name=":moneybag: Cash",
                    value=f"`{member['money']}$`"
                )

                embed.add_field(
                    name=":bank: Account",
                    value=f"`{member['bank']}$`"
                )

                embed.set_footer(text=f"Requested by {user.name}#{user.discriminator}")

                await interaction.followup.send(embed=embed)

                break
            
            else: pass
    

    @nextcord.slash_command(
        name="deposit",
        description="Deposit your money in the bank to be protected from thieves!"
    )
    async def deposit(
        self,
        interaction: nextcord.Interaction,
        amount: int = nextcord.SlashOption(
            name="amount",
            description="The amount of Dunk Dollars you want to deposit in your account.",
            required=True
        )
    ):
        await interaction.response.defer()
        members_data = economy_collection.find_one({"_id": interaction.guild.id})['members']
        
        final = None

        for member in members_data:
            if member['id'] == interaction.user.id:
                final = member

                if amount == 'all':
                    amount = member['money']

                    member['bank'] += amount
                    member['money'] -= amount

                    break
            
                elif int(amount) <= member['money']:
                    member['money'] -= int(amount)
                    member['bank'] += int(amount)

                    break
                
                else:
                    amount = member['money']
                    
                    member['money'] -= amount
                    member['bank'] += amount

                    break
            
            else:
                pass
        
        economy_collection.update_one(
            {"_id": interaction.guild.id},
            {"$set": {"members": members_data}}
        )

        embed = nextcord.Embed(
            title=":bank: Bank of Dunkville",
            description=f"Succesfully deposited {amount}$ in your bank account.",
            color=nextcord.Color.green()
        )

        embed.add_field(
            name=":moneybag: Cash",
            value=f"`{final['money']}$`"
        )

        embed.add_field(
            name=":bank: Account",
            value=f"`{final['bank']}$`"
        )

        await interaction.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
