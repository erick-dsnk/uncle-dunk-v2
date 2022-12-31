import random
import nextcord
from nextcord.ext import commands
from random import choice
import asyncpraw
import requests

from tokens import CLIENT_ID, CLIENT_SECRET, RAPID_API_KEY

reddit_instance = asyncpraw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent="Uncle Dunk's Bot/0.0.1 by u/dsnk24"
)

class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="8ball",
        description="Shake the Magic 8 Ball and get an answer to your question!"
    )
    async def _8ball(
        self,
        interaction: nextcord.Interaction,
        question: str = nextcord.SlashOption(
            name="question",
            description="The question you want to ask the Magic 8 Ball.",
            required=True
        )
    ):
        st_disagree_col = 0xff3100
        disagree_col = 0xfe9900
        neutral_col = 0xfece00
        agree_col = 0x8dd100
        st_agree_col = 0x00be0f

        st_agree_ans = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it."
        ]

        agree_ans = [
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes."
        ]

        neutral_ans = [
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
        ]
        
        disagree_ans = [
            "Don't count on it.",
            "My reply is no.",
            "My sources say no."
        ]

        st_disagree_ans = [
            "Outlook not so good.",
            "Very doubtful."
        ]


        resp_category = random.choice([st_agree_ans, agree_ans, neutral_ans, disagree_ans, st_disagree_ans])
        response = random.choice(resp_category)

        emb_col = 0x0

        if resp_category == st_agree_ans:
            emb_col = st_agree_col
        elif resp_category == agree_ans:
            emb_col = agree_col
        elif resp_category == neutral_ans:
            emb_col = neutral_col
        elif resp_category == disagree_ans:
            emb_col = disagree_col
        else:
            emb_col = st_disagree_col

        embed = nextcord.Embed(
            color=emb_col
        )

        embed.add_field(
            name=":question: Question",
            value=f"*{question}*"
        )

        embed.add_field(
            name=":a: Answer",
            value=f"*{response}*"
        )

        await interaction.response.send_message(embed=embed)
        
    @nextcord.slash_command(
        name="meme",
        description="It sends you a hot meme off Reddit!"
    )
    async def meme(
        self,
        interaction: nextcord.Interaction
    ):
        await interaction.response.defer(ephemeral=True)

        sub = random.choice([
            'memes',
            'ComedyCemetery',
            'MemeEconomy',
            'dankmemes',
            'terriblefacebookmemes',
            'funny',
            'raimimemes',
            'okbuddyretard',
            'comedyheaven'
        ])

        subreddit = await reddit_instance.subreddit(sub)
        
        submissions = []
        top = subreddit.top(limit=100)

        async for submission in top:
            submissions.append(submission)

        meme = random.choice(submissions)

        meme_name = meme.title
        meme_url = meme.url

        embed = nextcord.Embed(
            title=f'__{meme_name}__',
            colour=nextcord.Colour.random(),
            timestamp=interaction.created_at,
            url=meme_url
        )

        embed.set_image(url=meme_url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text='Here is your meme!')

        await interaction.followup.send(content=f"||<https://reddit.com/r/{sub}/>|| :white_check_mark:", embed=embed)


    # A cute doggo from reddit command :3
    @nextcord.slash_command(
        name="doggo",
        description="Sends you a picture of a cute doggo :3"
    )
    async def doggo(
        self,
        interaction: nextcord.Interaction
    ):
        await interaction.response.defer(ephemeral=True)

        sub = random.choice([
            'doggos',
            'dogpictures',
            'dogs',
            'puppies',
            'goldenretrievers'
        ])

        subreddit = await reddit_instance.subreddit(sub)
        
        submissions = []
        top = subreddit.top(limit=100)

        async for submission in top:
            submissions.append(submission)

        doggo = random.choice(submissions)

        doggo_name = doggo.title
        doggo_url = doggo.url

        embed = nextcord.Embed(
            title=f'__{doggo_name}__',
            colour=nextcord.Colour.random(),
            timestamp=interaction.created_at,
            url=doggo_url
        )

        embed.set_image(url=doggo_url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text='Here is your doggo!')

        await interaction.followup.send(content=f"||<https://reddit.com/r/{sub}/>|| :white_check_mark:", embed=embed)
    

    @nextcord.slash_command(
        name="kitty",
        description="Sends you a picture of a cute kitty :3"
    )
    async def kitty(
        self,
        interaction: nextcord.Interaction
    ):
        await interaction.response.defer(ephemeral=True)

        sub = random.choice([
            'JellyBeanToes',
            'CatsStandingUp',
            'Kittens',
            'Cats',
            'CatsInBusinessAttire',
            'TuckedInKitties'
        ])
        
        subreddit = await reddit_instance.subreddit(sub)
        
        submissions = []
        top = subreddit.top(limit=100)

        async for submission in top:
            submissions.append(submission)

        cat = random.choice(submissions)

        cat_name = cat.title
        cat_url = cat.url

        embed = nextcord.Embed(
            title=f'__{cat_name}__',
            colour=nextcord.Colour.random(),
            timestamp=interaction.created_at,
            url=cat_url
        )

        embed.set_image(url=cat_url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text='Here is your kitty!')

        await interaction.channel.send(content=f"||<https://reddit.com/r/{sub}/>|| :white_check_mark:", embed=embed)

    @nextcord.slash_command(
        name="joke",
        description="Tells you a top-notch joke."
    )
    async def joke(
        self,
        interaction: nextcord.Interaction
    ):
        await interaction.response.defer(ephemeral=True)

        url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"

        headers = {
            'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com",
            'x-rapidapi-key': RAPID_API_KEY
        }

        req = requests.get(url=url, headers=headers)

        joke_data = req.json()

        emb_title = choice([
            'Here\'s a good one!',
            'Ooo this is a spicy one!',
            'I\'m still laughing at this one!'
        ])

        emb_col = nextcord.Color.random()

        if joke_data['type'] == 'single':
            embed = nextcord.Embed(
                title=emb_title,
                color=emb_col,
                description=joke_data['joke']
            )

            await interaction.followup.send(embed=embed)
        
        elif joke_data['type'] == 'twopart':

            embed = nextcord.Embed(
                title=emb_title,
                color=emb_col,
                description=f"{joke_data['setup']}\n\n{joke_data['delivery']}"
            )

            await interaction.followup.send(embed=embed)

        else:
            await interaction.followup.send(":x: Something went wrong!")

    @nextcord.slash_command(
        name="pokemon",
        description="Get information about a Pokemon!"
    )
    async def pokemon(
        self,
        interaction: nextcord.Interaction,
        pokemon: str = nextcord.SlashOption(
            name="pokemon",
            description="The pokemon you want to get information on.",
            required=True
        )
    ):
        await interaction.response.defer(ephemeral=True)
        pokemon = pokemon.lower()
        response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)

        embed = nextcord.Embed()

        if response.status_code == 404:
            embed.title = "Darn!"
            embed.description = "Sorry, can't seem to find any information about that Pokemon. Check your spelling and try again!"
            embed.color = nextcord.Color.red()

        else:
            response = response.json()

            abilities = response['abilities']
            types = response['types']
            stats = response['stats']
            moves = response['moves']

            ability_field = ""
            type_field = ""
            stat_field = ""
            move_field = ""

            for ability in abilities:
                ability_field += ability['ability']['name'].title()
                ability_field += "\n"

            for _type in types:
                type_field += _type['type']['name'].title()
                type_field += "\n"

            for stat in stats:
                stat_field += stat['stat']['name'].title() + "\t\t" + str(stat['base_stat'])
                stat_field += "\n"

            if len(moves) > 6:
                for i in range(5):
                    move_field += moves[i]['move']['name'].title()
                    move_field += "\n"
                
                move_field += "..."
            
            else:
                for move in moves:
                    move_field += move['move']['name'].title()
                    move_field += "\n"

            embed.title = pokemon.title()
            embed.color = nextcord.Color.green()

            embed.add_field(
                name="**Height**",
                value=f"{response['height']}",
                inline=True
            )
            embed.add_field(
                name="**Weight**",
                value=f"{response['weight']}",
                inline=True
            )
            embed.add_field(
                name=f"**Types [{len(types)}**",
                value=f"{type_field}",
                inline=True
            )
            embed.add_field(
                name=f"**Abilities [{len(abilities)}]**",
                value=f"{ability_field}",
                inline=True
            )
            embed.add_field(
                name=f"**Stats**",
                value=f"{stat_field}",
                inline=True
            )
            embed.add_field(
                name=f"**Moves**",
                value=f"{move_field}",
                inline=True
            )

            embed.set_image(url=response['sprites']['back_default'])

        await interaction.followup.send(embed=embed)

def setup(bot):
    bot.add_cog(Entertainment(bot))
