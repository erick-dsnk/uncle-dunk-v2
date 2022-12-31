import nextcord
from nextcord.ext import commands


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="octal",
        description="Convert a number into its octal form."
    )
    async def octal(
        self,
        interaction: nextcord.Interaction,
        number: int = nextcord.SlashOption(
            name="number",
            description="The number you want to convert into an octal.",
            required=True
        )
    ):

        
        if number is not None:
            try:
                number = int(number)
            except Exception as e:
                print(f"An error occured while handling an octal command: {e}")

            if type(number) == int:
                embed = nextcord.Embed(
                    title="Octal Command",
                    description=f"The octal representation of `{number}` is: `{oct(number)}`"
                )
                await interaction.response.send_message(
                    embed=embed
                )
            else:
                await interaction.response.send_message(f":x: `{number}` is not an integer.")
        
        else:
            await interaction.response.send_message(":x: You didn't specify a number!")

    @nextcord.slash_command(
        name="binary",
        description="Convert a number into its binary form."
    )
    async def binary(
        self,
        interaction: nextcord.Interaction,
        number: int = nextcord.SlashOption(
            name="number",
            description="The number you want to convert into its binary form."
        )
    ):

        if number is not None:
            try:
                number = int(number)
            except Exception as e:
                print(f"An error occured while handling a binary command: {e}")


            if type(number) == int:
                embed = nextcord.Embed(
                    title="Binary Command",
                    description=f"The binary code of `{number}` is `{bin(number).replace('0b', '')}`"
                )

                await interaction.response.send_message(
                    embed=embed
                )
            else:
                await interaction.response.send_message(f":x: `{number}` is not an integer.")
            
        else:
            await interaction.response.send_message(":x: You didn't specify a number!")


    # Hexadecimal code of a number command
    @nextcord.slash_command(
        name="hexadecimal",
        description="Convert a number into its hexadecimal form."
    )
    async def hexadecimal(
        self,
        interaction: nextcord.Interaction,
        number: int = nextcord.SlashOption(
            name="number",
            description="Number you want to convert into its hexadecimal form."
        )
    ):  

        if number is not None:
            try:
                number = int(number)
            except Exception as e:
                print(f"An error occured while handling a hexadecimal command: {e}")
            

            if type(number) == int:
                embed = nextcord.Embed(
                    title="Hexadecimal Command",
                    description=f"The hexadecimal representation of `{number}` is {hex(number)}"
                )

                await interaction.response.send_message(
                    
                    f"The hexadecimal code of `{number}` is `{hex(number)}`"
                )
            else:
                await interaction.response.send_message(
                    embed=embed
                )
        
        else:
            await interaction.response.send_message(":x: You didn't specify a number!")


def setup(bot):
    bot.add_cog(Math(bot))

