# bot.py

import discord
from discord.ext import commands

TOKEN = open('token.txt', 'r').readline()

# client = discord.Client()
client = commands.Bot('.')


class application_manager:

    def __init__(self):
        self.responses = []
        self.application = {}
        print(bool(self.application))

    def addResponse(self, message):
        self.message = message
        self.responses.append(self.message)

    def compile(self, discord_id):
        self.application[f'{discord_id}'] = self.responses

    def fetch(self, discord_id):
        return self.application[f'{discord_id}']
        print(bool(self.application))

    def fetchAll(self):
        return self.application
        print(bool(self.application))

    def checkDict(self):
        return bool(self.application)


# @client.command(name='helpme')
# async def help(context):
#     help_embed = discord.Embed(title='Help', description='Command list for the application bot', color=0xff0000) # noqa
#     help_embed.add_field(name='.apply', value='To begin an application process', inline=True) # noqa
#     help_embed.add_field(name='.helpme', value='To view this help message', inline=True) # noqa
#     help_embed.set_author(name='BABAji')
#     help_embed.set_footer(text='For further queries or Bug Reports DM BABAji')

#     await context.message.channel.send(embed=help_embed)


questions = [
            "1. What is your Call of Duty: Mobile IGN (In-Game Name)?",
            "2. How old are you?",
            "3. Which region are you from? (Example: NA or EU)",
            "4. What time do you usually play? (Example: 2200 hrs CST)",
            "5. What are your Current and Personal Best ranks respectively?",
            "6. BR or MP: Which one do you prefer more?",
            "7. Number of matches you play per day (on an average)?",
            "8. How would you describe yourself as a player (Casual or Competitive)?", # noqa
            "9. What is your preferred weapon class?",
            "10. Would you be willing to use voice communication during ranked matches or Clan in-house scrims?", # noqa
            "11. In brief, describe why do you wanna join us and what would be willing to offer to the clan?", # noqa
            "12. Make your in-game profile and battle logs unhidden. It might take 1-2 days for your application to be reviewed by the Recruiters (we promise to do it ASAP). Please type anything to continue." # noqa
            ]


@client.command(name='apply')
async def apply(context):

    await context.send('Fill the application through your DMs')
    apply_embed = discord.Embed(title='Enchiladas Application', description='So you wanna apply for the clan! Good choice\nAnswer the following questions to finish the application', color=0x00ff00) # noqa
    await context.message.author.send(embed=apply_embed) # noqa

    mngr = application_manager()
    for question in questions:
        await context.message.author.send(question)
        resp = await client.wait_for('message')
        mngr.addResponse(resp.content)
    await context.message.author.send(embed=discord.Embed(description='Finished application', color=0x00ff00))

    # await context.message.author.send("So this is your application:\n")
    # await context.message.author.send()
    # await context.message.author.send("Do you wanna send this? (y/n)")


@client.command(name='review')
async def review(context):
    mngr = application_manager()
    if mngr.checkDict is False:
        await context.message.channel.send(embed=discord.Embed(title='No applications to review', color=0x00ff00))
    else:
        await context.message.author.send(embed=discord.Embed(title='Enter the discord id of applicant you wanna review', color=0x00ff00))

        id = await client.wait_for('message')
        await context.message.author.send(mngr.fetch(id))


@client.command(name='reviewAll')
async def reviewAll(context):
    mngr = application_manager()
    if mngr.checkDict is False:
        await context.message.author.send(embed=discord.Embed(title='No applications to review', color=0x00ff00))
    else:
        await context.message.author.send(mngr.fetchAll())


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='.help'))
    print(f'{client.user} has connected to Discord!')

    # general_channel = client.get_channel(758167336544239640)
    # await general_channel.send('Baba ki jai ho!')


@client.event
async def on_message(message):
    if 'baba' in message.content:
        # general_channel = client.get_channel(758167336544239640)
        # await general_channel.send('Baba ki jai ho!')
        await message.channel.send("Baba ki jai ho!")   # This will work for all channels Unlike the above code that would only work for general channel # noqa

    elif 'babaji' in message.mentions:
        await message.channel.send("Who dares!!!")

    await client.process_commands(message)

client.run(TOKEN)
