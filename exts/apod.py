from typing import Dict, Any
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot
from datetime import date
import requests
import time
import random

from tokens import NASA_API_KEY

class Apod:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.url = "https://api.nasa.gov/planetary/apod"
        self.date = None
    
    def fetch_apod_data(self) -> Dict:
        start_time = time.mktime(time.strptime("2016-1-1", "%Y-%m-%d"))
        end_time = time.mktime(time.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d"))

        random_time = start_time + random.random() * (end_time-start_time)

        self.date = time.strftime("%Y-%m-%d", time.gmtime(random_time))

        headers = {
            'api_key': self.api_key,
            'date': self.date,
            'hd': True
        }

        response = requests.get(
            url=self.url,
            params=headers
        ).json()

        return response
    

    def get_image(self) -> Any:
        data = self.fetch_apod_data()
        return data['hdurl'], data['title'], self.date



class ApodCommand(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        self.apod_instance = Apod(api_key=NASA_API_KEY)
    

    @nextcord.slash_command(
        name="space",
        description="Sends an image from NASA that was taken today!"
    )
    async def space(
        self,
        interaction: nextcord.Interaction,
        visible: bool = nextcord.SlashOption(
            name="visible",
            description="Whether you want the command to be visible to others or not.",
            required=False,
            default=True
        )
    ):  
        await interaction.response.defer(ephemeral = not visible)

        url, title, _date = self.apod_instance.get_image()

        embed = nextcord.Embed(
            title=f"**{title}**",
            description=f"**{_date}**",
            color=nextcord.Color.dark_blue()
        )

        embed.set_image(url=url)
        
        embed.set_footer(
            text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}",
            icon_url=interaction.user.avatar.url
        )

        await interaction.followup.send(embed=embed)
        


def setup(bot):
    bot.add_cog(ApodCommand(bot))