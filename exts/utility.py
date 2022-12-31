import os
import nextcord
from nextcord.ext import commands
from newsapi import NewsApiClient
import requests
import psutil

from tokens import NEWS_API_KEY, WEATHER_API_KEY, RAPID_API_KEY

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="ping",
        description="Display the latency of the bot!"
    )
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(f":ping_pong: Pong! Time took to respond: `{round(self.bot.latency * 1000)}ms`")


    @nextcord.slash_command(
        name="news",
        description="Get the latest news on the specified topic!"
    )
    async def news(
        self,
        interaction: nextcord.Interaction,
        topic: str = nextcord.SlashOption(
            name="topic",
            description="The topic of the news you want to see.",
            required=False,
            default=""
        )
    ):
        await interaction.response.defer(ephemeral=True)

        news_src = "abc-news,associated-press,axios,bleacher-report,bloomberg,breitbart-news,business-insider,buzzfeed,cbs-news,cnn,crypto-coins-news,engadget,entertainment-weekly,espn,fox-news,fox-sports,google-news,hacker-news,ign,mashable,medical-news-today,msnbc,mtv-news,national-geographic,national-review,nbc-news,new-scientist,newsweek,new-york-magazine,next-big-future,nfl-news,nhl-news,politico,polygon,recode,reddit-r-all,reuters,techcrunch,techradar,the-american-conservative,the-hill,the-huffington-post,-weekly,espn,espn-cric-info,fortune,fox-news,fox-sports,google-news,hacker-news,ign,mashable,medical-news-today,msnbc,mtv-news,national-geographic,national-review,nbc-news,new-scientist,newsweek,new-york-magazine,next-big-future,nfl-news,nhl-news,politico,polygon,recode,reddit-r-all,reuters,techcrunch,techradar,the-american-conservative,the-hill,the-huffington-post,the-next-web,the-verge,the-wall-street-journal,the-washington-post,the-washington-times,time,usa-today,vice-news,wired"

        articles = None

        if topic != "":
            top_headlines = newsapi.get_top_headlines(
                q=topic,
                sources=news_src,
                language="en"
            )
            articles = top_headlines['articles']
        else:
            top_headlines = newsapi.get_top_headlines(
                sources="abc-news,associated-press,axios,bleacher-report,bloomberg,breitbart-news,business-insider,buzzfeed,cbs-news,cnn,crypto-coins-news,engadget,entertainment-weekly,espn,fox-news,fox-sports,google-news,hacker-news,ign,mashable,medical-news-today,msnbc,mtv-news,national-geographic,national-review,nbc-news,new-scientist,newsweek,new-york-magazine,next-big-future,nfl-news,nhl-news,politico,polygon,recode,reddit-r-all,reuters,techcrunch,techradar,the-american-conservative,the-hill,the-huffington-post,-weekly,espn,espn-cric-info,fortune,fox-news,fox-sports,google-news,hacker-news,ign,mashable,medical-news-today,msnbc,mtv-news,national-geographic,national-review,nbc-news,new-scientist,newsweek,new-york-magazine,next-big-future,nfl-news,nhl-news,politico,polygon,recode,reddit-r-all,reuters,techcrunch,techradar,the-american-conservative,the-hill,the-huffington-post,the-next-web,the-verge,the-wall-street-journal,the-washington-post,the-washington-times,time,usa-today,vice-news,wired",
                language="en"
            )
            articles = top_headlines['articles']

        embed = nextcord.Embed(
            title=f":newspaper: Top headlines I could find!",
            color=nextcord.Color.blurple()
        )

        for i in range(3):
            embed.add_field(
                name=f"\n**{i+1}. {articles[i]['title']}**",
                value=f"{articles[i]['description']}\n\nRead more [here]({articles[i]['url']})\n"
            )

        embed.set_footer(text='Powered by NewsAPI.')

        await interaction.followup.send(embed=embed)

    @nextcord.slash_command(
        name="weather",
        description="Sends you the latest weather forecast in a city or country."
    )
    async def weather(
        self,
        interaction: nextcord.Interaction,
        location: str = nextcord.SlashOption(
            name="location",
            description="The city or country for which you want to see the weather forecast.",
            required=True
        )
    ):
        await interaction.response.defer()

        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric'

        response = requests.get(url=url)

        data = response.json()

        additional_data = data['weather']
        desc = additional_data[0]['description']

        weather_data = data['main']

        curr_temp = weather_data['temp']
        feels_like_temp = weather_data['feels_like']
        humidity = weather_data['humidity']
        atmospheric_pressure = weather_data['pressure']

        wind_data = data['wind']
        wind_speed = wind_data['speed']

        clouds_data = data['clouds']
        cloudiness = clouds_data['all']

        city_data = data['name']

        embed = nextcord.Embed(
            title=f'Weather data for {city_data}',
            colour=nextcord.Color.from_rgb(43, 223, 255)
        )

        embed.add_field(
            name="**:white_sun_cloud:  Basic weather**",
            value=f'**Description**: {desc}\n**Current temperature**: {curr_temp}\n**What it feels like**: {feels_like_temp}'
        )

        embed.add_field(
            name="**:cloud: Wind speed, Humidity, etc**",
            value=f"**Wind speed**: {wind_speed} m/s\n**Humidity**: {humidity}%\n**Cloudiness**: {cloudiness}%\n**Atmospheric Pressure**: {round((atmospheric_pressure / 1013.25), 4)} atm ({atmospheric_pressure} hPa)"
        )

        await interaction.followup.send(embed=embed)

    @nextcord.slash_command(
        name="covid",
        description="Get information about the latest COVID-19 pandemic situation in a country."
    )
    async def corona(
        self,
        interaction: nextcord.Interaction,
        country: str = nextcord.SlashOption(
            name="location",
            description="The country of which you want to see the COVID situation.",
            required=True
        )
    ):  
        await interaction.response.defer()
        
        try:
            response = requests.request(
                "GET",
                "https://covid-193.p.rapidapi.com/statistics",
                headers={
                    'x-rapidapi-host': "covid-193.p.rapidapi.com",
                    'x-rapidapi-key': RAPID_API_KEY
                },
                params={
                    "country": country
                }
            )

            covid_data = response.json()

            data = covid_data['response'][0]
            
            cases_data = data['cases']
            death_data = data['deaths']

            loc = f"{data['country']}, {data['continent']}"
            total_cases = cases_data['total']
            new_cases = cases_data['new']
            healed_cases = cases_data['recovered']
            active_cases = cases_data['active']

            new_deaths = death_data['new']
            total_deaths = death_data['total']

            date = data['day']

            embed = nextcord.Embed(
                title=f":microbe: **COVID-19 statistics for {loc}**",
                color=nextcord.Color.dark_gold()
            )

            embed.add_field(
                name=":mask: Cases",
                value=f"Total: `{total_cases}`\nActive: `{active_cases}`\nNew: `{new_cases}`"
            )

            embed.add_field(
                name=":grin: Recovered",
                value=f"`{healed_cases}`"
            )

            embed.add_field(
                name=":skull: Deaths",
                value=f"Total: `{total_deaths}`\nNew: `{new_deaths}`"
            )

            embed.set_footer(text=f"Date: {date}")

            await interaction.followup.send(embed=embed)

        
        except Exception as e:
            await interaction.followup.send(":x: Sorry, I can't seem to fetch any information about it.")

            print(e)

    @nextcord.slash_command(
        name="avatar",
        description="Like a person's profile picture? You can now get it with this command!"
    )
    async def avatar(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            name="member",
            description="The user you want to get the avatar of. Leave empty if you want to get your avatar.",
            required=False,
            default=None
        )
    ):
        if member is None:
            member = interaction.user

        embed = nextcord.Embed(
            title=f":frame_photo: **{member.name}#{member.discriminator}'s profile picture:**"
        )
        embed.set_image(url=member.avatar.url)

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="botinfo",
        description="Get information about the bot and its status."
    )
    async def botinfo(
        self,
        interaction: nextcord.Interaction
    ):
        user = await self.bot.fetch_user(419022467210936330)
        icon = user.avatar.url
        embed = nextcord.Embed(
            title="**Bot Info**",
            description="\n",
            color=nextcord.Color.green()
        )
        embed.add_field(
            name=":desktop: **Memory Usage**",
            value=f"CPU Usage: `{psutil.cpu_percent()}%`\nVRAM Usage: `{psutil.virtual_memory().percent}%`",
            inline=True
        )
        embed.add_field(
            name=":floppy_disk: **Bot's Developer**",
            value="`dsnk#5622`",
            inline=True
        )
        embed.add_field(
            name=":shield: **Servers**",
            value=f"`{len(self.bot.guilds)}`",
            inline=True
        )
        embed.add_field(
            name=":tools: **Source and Framework**",
            value="Framework: `nextcord` (migrated from discord.py)\nSource: [Go to GitHub](https://github.com/erick-dsnk/uncle-dunks-discord-bot)",
            inline=True
        )
        embed.add_field(
            name=":robot: Version",
            value="v2.0.0",
            inline=True
        )
        embed.set_footer(
            text="Developed by dsnk#5622",
            icon_url=icon
        )

        await interaction.response.send_message(embed=embed)
    

    @nextcord.slash_command(
        name="userinfo",
        description="Get information about a certain user!"
    )
    async def userinfo(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The user you want to display information about.",
            required=False,
            default=None
        )
    ):
        if user is None: user = interaction.user

        joined = user.joined_at.strftime('`%d-%m-%Y @ %H:%M:%S`')
        created = user.created_at.strftime('`%d-%m-%Y @ %H:%M:%S`')

        embed = nextcord.Embed(
            title=f"{user.name}#{user.discriminator}",
            description="\n",
            color=nextcord.Color.green()
        )

        embed.add_field(
            name=":clock: **Basic**",
            value=f"Joined server: {joined}\nCreated account: {created}",
            inline=True
        )

        embed.add_field(
            name=":military_medal: **Top Role:**",
            value=f"{user.top_role.mention}",
            inline=True
        )


        if user.status == nextcord.Status.online:
            embed.add_field(
                name=":moyai: **User Status**",
                value="(*) :green_circle: Online\n( ) :red_circle: Do Not Disturb\n( ) :black_circle: Offline/Invisible"
            )
        
        elif user.status == nextcord.Status.idle:
            embed.add_field(
                name=":moyai: **User Status**",
                value="( ) :green_circle: Online\n(*) :yellow_circle: Idle\n( ) :red_circle: Do Not Disturb\n( ) :black_circle: Offline/Invisible"
            )

        elif user.status == nextcord.Status.do_not_disturb:
            embed.add_field(
                name=":moyai: **User Status**",
                value="( ) :green_circle: Online\n( ) :yellow_circle: Idle\n(*) :red_circle: Do Not Disturb\n( ) :black_circle: Offline/Invisible"
            )        
        
        elif user.status == nextcord.Status.offline or user.status == nextcord.Status.invisible:
            embed.add_field(
                name=":moyai: **User Status**",
                value="( ) :green_circle: Online\n( ) :yellow_circle: Idle\n( ) :red_circle: Do Not Disturb\n(*) :black_circle: Offline/Invisible"
            )
        

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="serverinfo",
        description="Get information about the server the command was used in."
    )
    async def serverinfo(
        self,
        interaction: nextcord.Interaction
    ):
        embed = nextcord.Embed(
            color=nextcord.Color.dark_blue()
        )
        c = 0
        b = 0
        for i in interaction.guild.members:
            if i.bot:
                b = b + 1
            else:
                c = c + 1

        offline = 0
        online = 0
        idle = 0
        dnd = 0

        for user in interaction.guild.members:
            if user.status == nextcord.Status.offline:
                offline += 1
            
            elif user.status == nextcord.Status.online:
                online += 1

            elif user.status == nextcord.Status.idle:
                idle += 1

            elif user.status == nextcord.Status.dnd:
                dnd += 1

        if interaction.guild.icon is not None:
            embed.set_thumbnail(url=interaction.guild.icon.url)

        embed.set_author(
            name='Server Info',
            icon_url='https://www.trendmicro.com/azure/wp-content/uploads/2015/11/TM_ServerSequence_300x300.gif'
        )

        embed.add_field(
            name=":ballot_box: Name:",
            inline=True,
            value=f"**{interaction.guild.name}**"
        )

        embed.add_field(
            name=":crown: Owner:", inline=True,
            value=f"{interaction.guild.owner.name}#{interaction.guild.owner.discriminator}"
        
        )
        embed.add_field(
            name=":credit_card: Server ID",
            inline=True,
            value=f'`{interaction.guild.id}`'
        )

        embed.add_field(
            name=":person_pouting: Members: ",
            inline=True,
            value=f"`{c}`"
        )

        embed.add_field(
            name=":robot: Bots: ",
            inline=True,
            value=f"`{b}`"
        )

        embed.add_field(
            name="Online: ",
            inline=True,
            value=f":green_circle:  `{online}`"
        )

        embed.add_field(
            name="Idle: ",
            inline=True,
            value=f":yellow_circle:  `{idle}`"
        )

        embed.add_field(
            name="Do not disturb: ",
            inline=True,
            value=f":red_circle:  `{dnd}`"
        )

        embed.add_field(
            name="Offline : ",
            inline=True,
            value=f":black_circle:  `{offline}`"
        )

        embed.add_field(
            name=":calendar: Server created at: ",
            value=f"{interaction.guild.created_at.strftime('%A, %B , `%d` : `%Y` @ `%H:%M:%S` UTC')}",
            inline=False
        )

        embed.add_field(
            name=":printer:  Text Channels:",
            inline=True,
            value=f"`{len(interaction.guild.text_channels)}`"
        )

        embed.add_field(
            name=":microphone2:  Voice Channels:",
            inline=True,
            value=f"`{len(interaction.guild.voice_channels)}`"
        )

        embed.add_field(
            name="Roles: ",
            inline=True,
            value=f'`{len(interaction.guild.roles)}`'
        )

        embed.set_footer(
            icon_url=interaction.user.avatar.url,
            text=f"Requested by {interaction.user.name}#{interaction.user.discriminator} on {interaction.created_at.strftime('%A %B %d %Y @ %H:%M:%S %p')}"
        )

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="topgg",
        description="Check out my top.gg page!"
    )
    async def topgg(
        self,
        interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("My top.gg page! https://top.gg/bot/743859839821807736")
    

    @nextcord.slash_command(
        name="changelog",
        description="Show what's new with Uncle Dunk!"
    )
    async def changelog(
        self,
        interaction: nextcord.Interaction
    ):
        await interaction.response.defer()
        
        with open(os.path.abspath('changelog.txt'), 'r') as f:
            changelog_message = f.read()

        embed = nextcord.Embed(
            title=':robot: Uncle Dunk Changelog!',
            description=changelog_message,
            color=nextcord.Color.green()
        )

        await interaction.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
