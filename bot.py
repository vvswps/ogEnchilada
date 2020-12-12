# bot.py

import discord
from discord.ext import commands
import json


# client = discord.Client()
client = commands.Bot('.', help_command=None)


questions = [
            "1. What is your Call of Duty: Mobile IGN (In-Game Name)?",
            "2. How old are you?",
            "3. Which region are you from? (Example: NA or EU)",
            "4. What time do you usually play? (Example: 2200 hrs CST)",
            "5. What are your Current and Personal Best ranks respectively?",
            "6. BR or MP: Which one do you prefer more?",
            "7. Number of matches you play per day (on an average)?",
            "8. How would you describe yourself as a player (Casual or Competitive)?",
            "9. What is your preferred weapon class?",
            "10. Would you be willing to use voice communication during ranked matches or Clan in-house scrims?",
            "11. In brief, describe why do you wanna join us and what would be willing to offer to the clan?",
            "12. Make your in-game profile and battle logs unhidden. It might take 1-2 days for your application to be reviewed by the Recruiters (we promise to do it ASAP). Please type anything to continue."
            ]


class application_manager:

    def __init__(self):
        self.responses = []
        d = open('data.json', 'r+')
        self.application = json.load(d)
        self.current_app = {}
        # print(bool(self.application))

    def addResponse(self, message):
        self.responses.append(message)

    def compile(self, discord_id):
        e = dict(zip(questions, self.responses))
        self.current_app[f'{discord_id}'] = e

    def fetch(self, discord_id):
        return self.application[f'{discord_id}']
        # print(bool(self.application))

    def fetchAll(self):
        for appln in self.application:
            return appln
        # print(bool(self.application))

    def check(self):
        return bool(self.application)


@client.command(name='help')
async def help(context):
    help_embed = discord.Embed(title='Help', description='Command list for the application bot', color=0x101020)

    help_embed.add_field(name='.apply', value='To begin an application process', inline=True)

    help_embed.add_field(name='.helpme', value='To view this help message', inline=True)

    help_embed.set_author(name='BABAji')
    help_embed.set_footer(text='For further queries or Bug Reports DM BABAji')

    await context.message.channel.send(embed=help_embed)


@client.command(name='apply')
async def apply(context):

    await context.send('Fill the application through your DMs')
    apply_embed = discord.Embed(title='Enchiladas Application', description='So you wanna apply for the clan! Good choice\nAnswer the following questions to finish the application', color=0x00ff00)

    await context.message.author.send(embed=apply_embed)

    mngr = application_manager()
    for question in questions:
        await context.message.author.send(question)
        while 0 < 1:
            resp = await client.wait_for('message')
            if resp.author == context.message.author:
            # if resp.content != question:
                print(resp.content)
                mngr.addResponse(resp.content)
                break
            else:
                # await context.message.author.send("Sorry some error occurred")
                continue

    mngr.compile(context.message.author)
    await context.message.author.send(embed=discord.Embed(description='Finished application', color=0x00ff00))

    # await context.message.author.send("So this is your application:\n")
    # await context.message.author.send()
    # await context.message.author.send("Do you wanna send this? (y/n)")


@client.command(name='review')
async def review(context):
    mngr = application_manager()
    if mngr.check is False:
        await context.message.channel.send(embed=discord.Embed(title='No applications to review', color=0x00ff00))
    else:
        await context.message.author.send(embed=discord.Embed(title='Enter the discord id of applicant you wanna review', color=0x00ff00))

        id = await client.wait_for('message')
        await context.message.author.send(mngr.fetch(id))


@client.command(name='reviewAll')
async def reviewAll(context):
    mngr = application_manager()
    if mngr.check is False:
        await context.message.author.send(embed=discord.Embed(title='No applications to review', color=0x00ff00))
    else:
        await context.message.author.send(mngr.fetchAll())


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='.help'))
    print(f'{client.user} has connected to Discord!')

    # general_channel = client.get_channel(channel_id)
    # await general_channel.send('Baba ki jai ho!')


@client.event
async def on_message(message):
    if 'baba' in message.content:
        # general_channel = client.get_channel(channel_id)
        # await general_channel.send('Baba ki jai ho!')
        await message.channel.send("Baba ki jai ho!")   # This will work for all channels Unlike the above code that would only work for general channel

    elif 'babaji' in message.mentions:
        await message.channel.send("Who dares!!!")

    await client.process_commands(message)


with open('token.txt', 'r') as TOKEN:
    client.run(TOKEN.readline())
