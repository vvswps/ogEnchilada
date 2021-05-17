import os
import asyncio
import json
import discord
from discord.channel import DMChannel
from discord.ext import commands
from discord.utils import get
from random import choice

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


def fetch():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        pass


def addResponses(list, discord_id):
    data = fetch()
    print(type(data))
    data[discord_id] = list
    try:
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as ex:
        print(ex)


def removeEntry(id):
    data = fetch()
    data.pop(id)
    try:
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as ex:
        print(ex)


@client.command(name='help')
async def help(context):
    help_embed = discord.Embed(title='Help', description='Command list for the application bot', color=0x00b4d8)

    help_embed.add_field(name='.apply', value='To begin an application process', inline=True)

    help_embed.add_field(name='.review', value='To review submitted applications', inline=True)
    help_embed.add_field(name='.aplist', value='To list all submitted applications', inline=True)
    help_embed.add_field(name='.help', value='To view this help message', inline=True)

    help_embed.set_author(name='BABAji')
    help_embed.set_footer(text='For further queries or Bug Reports DM BABAji')

    await context.message.channel.send(embed=help_embed)


@client.command(name='apply')
async def apply(context):
    if isinstance(context.message.channel, DMChannel):
        await context.send(embed=discord.Embed(title='Error', description="This command isn't avaliable in dms", color=0x00ff00))
        return

    resp_list = []
    await context.send('Fill the application through your DMs')
    apply_embed = discord.Embed(title='Enchiladas Application', description='So you wanna apply for the clan! Good choice\nAnswer the following questions to finish the application', color=0x00ff00)

    await context.message.author.send(embed=apply_embed)

    for question in questions:
        await context.message.author.send(question)

        def check(m):
            return m.author == context.message.author

        resp = await client.wait_for('message', check=check, timeout=60.0)
        resp_list.append(resp.content)

    await context.message.author.send(embed=discord.Embed(description='Finished application', color=0x00ff00))
    try:
        author = str(context.message.author)
        addResponses(resp_list, author)
    except Exception as ex:
        print(ex)
    print(resp_list)


@client.command(name='review')
async def review(context):
    answers = []
    try:
        id = f'{context.message.mentions[0].name}#{context.message.mentions[0].discriminator}'
        try:
            answers = fetch()[id]
        except IndexError:
            context.channel.send("No Applications to review")
            return

    except Exception as ex:
        print(ex)

    try:
        app_embed = discord.Embed(title=id, descrption=f"{id}'s application for the clan", colour=0x2a9d8f)
        for i in range(len(questions)):
            app_embed.add_field(name=questions[i], value=answers[i], inline=True)
        app_embed.set_footer(text=f"To accept react with {'✔'} to reject {'❌'} or {'🔴'} if you want to stop review")
        app_msg = await context.channel.send(embed=app_embed)
        await app_msg.add_reaction('✔')
        await app_msg.add_reaction("❌")
        await app_msg.add_reaction('🔴')
    except Exception as ex:
        print(ex)

    def check(reaction, user):
        return user == context.author and (str(reaction.emoji) == '✔' or str(reaction.emoji) == '❌' or str(reaction.emoji) == '🔴')

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=90.0, check=check)
    except asyncio.TimeoutError:
        await context.channel.send("Timeout")
    if reaction.emoji == '✔':
        try:
            await context.channel.send("Application Accepted\nApplicant was given the 'New applicant role' which will be automatically removed after a minute")
            await context.message.mentions[0].send("Congrats! Your application for The Enchiladas was ACCEPTED\nDon't forget to come for tryouts on time\nYou have been given the 'New Applicant' role which will last for a minute you can come for tryouts during that time or you'll have to start the application process again")
            role = get(context.guild.roles, name='New applicant')
            await context.message.mentions[0].add_roles(role)

            removeEntry(str(id))
            await asyncio.sleep(60.0)
            await context.message.mentions[0].remove_roles(role)
        except Exception as ex:
            print(ex)

    elif reaction.emoji == '❌':
        try:
            await context.channel.send("Please provide a reason")

            def check_msg(message):
                return message.author == context.author

            try:
                msg = await client.wait_for("message", check=check_msg, timeout=90.0)
            except asyncio.TimeoutError:
                await context.channel.send("Timeout")
            await context.message.mentions[0].send(f"Sadly your application for The Enchiladas was declined with the following reason: {msg.content}")
            removeEntry(str(id))
            await context.channel.send("Declined Successfully")
        except Exception as ex:
            print(ex)

    elif reaction.emoji == '🔴':
        try:
            await context.channel.send("Stopped reviewing")
            return
        except Exception as ex:
            print(ex)


@client.command(name='aplist')
async def aplist(context):
    with open("data.json", 'r') as file:
        data = json.load(file)
    await context.channel.send(embed=discord.Embed(title="Here's a list of applications not yet reviewed", description='\n'.join([i for i in data.keys()])))


@client.event
async def on_command_error(context, exception):
    if isinstance(exception, commands.CommandNotFound):
        await context.message.delete()
        await context.send(embed=discord.Embed(description='No such command exists. Try .help', color=0x0000ff))


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='.help'))
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if 'baba' in message.content.lower() and message.author != client.user:
        await message.channel.send(choice(["Baba ki jai ho!", "Babaji ki booti...", "Doing yoga", "Smoking neem"]))

    if 'ding' in message.content.lower() and message.author != client.user:
        await message.channel.send(choice(["DingDong!", "Who's there", "😐", "😑", "🤔", "Ding ma Dong😏"]))

    if 'pyro' in message.content.lower() and message.author != client.user:
        await message.channel.send(choice(["AAG laga doonga", "Fire burns", "💥", "🔥", "☔", "Hot af😏"]))

    if 'nish' in message.content.lower() and message.author != client.user:
        await message.channel.send(choice(["nishimabb", "BB", "❤", "💖", "💗", "💘", "Dua😏"]))

    if 'lixio' in message.content.lower() and message.author != client.user:
        await message.channel.send(choice(["Simp", "😎", "😃", "🥱", "😏"]))

    if 'shady' in message.content.lower() and message.author != client.user:
        await message.channel.send(choice(["Aye merwinnn", "I've got you in ma sights", "🥴", "🤓", "👻", "😈", "👹", "👺", "👁", "💢", "☢"]))

    if '613451817510109205' in message.content and message.author != client.user:
        await message.channel.send(choice(["Who Dares!!!", "You sure you wanted to tag him💀👹", "You want some 'Guruji ka pyar?'😏"]))

    await client.process_commands(message)


client.run(os.getenv("TOKEN"))
