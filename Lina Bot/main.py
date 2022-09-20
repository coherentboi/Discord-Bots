import discord
from discord.ext import commands
import os
import json
import asyncio

client = commands.Bot(command_prefix = '$', case_insensitive=True)
client.remove_command('help')

subjects=[]

with open('subjects.json') as f:
    data = json.load(f)

for name in data["subjects"]:
    subjects.append(name)

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('$help'))
  print('Bot is ready')


#Access the help menu
@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = 'Bot Help',
    description = '{} used $help.'.format(ctx.author),
    colour = discord.Colour.blue()
  )
  embed.add_field(name = "Check out our commands!", value = "<https://docs.google.com/document/d/1yHXLGB7gVD0u52oWhVVbOTfZogNATmCWRu0slDmsJcI/edit>", inline = False)
  embed.set_footer(text='Message ...Awkward#0252 if something is not working.')
  embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
  await ctx.send(embed=embed)

#Mentor Registration Command
@client.command(aliases = ["registerMentor","registerM","m"])
async def registerAsMentor(ctx):

    blacklist = await get_blacklist()
    if str(ctx.author.id) in blacklist:
        await ctx.send("You have been blacklisted and therefore cannot use the bot's commands. Use $appeal to schedule an appeal.")
        return

    users = await get_mentors()

    if str(ctx.author.id) in users:
        await ctx.send('You are already registered!')
        return

    rules = discord.Embed(
        title = "Mentor Rules",
        colour = discord.Colour.blue()
    )
    rules.add_field(name = "Rules", value="1. Be respectful, common sense stuff. \n \n 2. No cursing or vulgar language \n \n3. No question is a dumb question, don't make fun of someone for a question they have. \n \n4. If you don't know the answer to a question don't answer it. \n \n5. Use the bot for school help only. \n \n6. Students do not owe mentors anything. \n\n React with ✅ if you understand.", inline = False)
    message = await ctx.send(embed = rules)
    await message.add_reaction("✅")

    def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'

    reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check)

    try:
        await registration(ctx.author)
        await ctx.send("Your account has been successfully registered.")
        await user.send("Your mentor account has been registered!")
    except:
        await ctx.send("Something went wrong.")


#Question Asking Command
@client.command(aliases = ["ask","askquestion"])
async def question(ctx):

    blacklist = await get_blacklist()
    if str(ctx.author.id) in blacklist:
        await ctx.send("You have been blacklisted and therefore cannot use the bot's commands. Use $appeal to schedule an appeal.")
        return

    mentors = await get_mentors()

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send('Please input the subject you need help in! (Type "Exit" to exit at any point.)')

    while (True):
        message = await client.wait_for("message",check = check)
        subject = message.content.lower()
        subject = subject.capitalize()
        if subject.lower() == "$ask":
            await ctx.send("Exited")
            return
        if subject.lower() == "exit":
            await ctx.send("Exited")
            return
        elif subject in subjects:
            break
        else:
            await ctx.send("This is not a valid subject. Please try again or contact ...Awkward#0252.")

    await ctx.send('Please input the question you would like to ask!')

    message = await client.wait_for("message",check = check)

    question = message

    if question.content.lower() == "$ask":
        await ctx.send("Exited")
        return
    if question.content.lower() == "exit":
        await ctx.send("Exited")
        return

    mentors_to_ping = await find_available_mentors(subject, ctx.author.id)

    if len(mentors_to_ping) == 0:
        await ctx.send("Sorry, but we cannot find any mentors at the moment.")
    else:
        await ctx.send("Found {} mentor(s). Messaging them now. All given answers will be returned to you in your direct messages.".format(len(mentors_to_ping)))

    for i in mentors_to_ping:
        member = await client.fetch_user(i)
        await dm(member, ctx.author.id,subject,ctx.author,question)

#DM Function
async def dm(member,id,subject,mentee,question):
    try:
        message = await member.send("Subject: `{}`. Question: \n \n '{}'{} \n \n To help, simply use the discord reply function and reply to this message with the answer within 30 minutes".format(subject, question.content, question.attachments[0].url))
    except:
        message = await member.send("Subject: `{}`. Question: \n \n '{}' \n \n To help, simply use the discord reply function and reply to this message with the answer within 30 minutes".format(subject, question.content))
    await log_message(mentee, question, message)
    def check(m):
        if m.reference is not None:
            if m.reference.message_id == message.id:
                if m.content.startswith("$report"):
                    return False
                return True
        return False
    answer = await client.wait_for("message",check = check, timeout = 1800)
    await member.send("Thank you for your answer! It has been sent to the person.")
    reply = await client.fetch_user(id)
    try:
        message2 = await reply.send("Response to your question `{}` was: \n \n '{}'{} \n \n Please rate this answer on a scale of 1-10! To do so, simply use the discord reply function and reply to this message with a rating from 1-10 within 15 minutes.".format(question.content, answer.content, answer.attachments[0].url))
    except:
        message2 = await reply.send("Response to your question `{}` was: \n \n '{}' \n \n Please rate this answer on a scale of 1-10! To do so, simply use the discord reply function and reply to this message with a rating from 1-10 within 15 minutes.".format(question.content, answer.content))
    await log_message(member, answer, message2)
    def check2(m):
        try:
            test = int(m.content)
            if test < 1 or test > 10:
                return False
        except:
            return False
        if m.reference is not None:
            if m.content.startswith("$report"):
                return False
            if m.reference.message_id == message2.id:
                return True
    rating = await client.wait_for("message",check = check2, timeout = 900)
    await reply.send("Thank you for your feedback!")
    await add_points(int(rating.content), member.id)



#Points system function
async def add_points(rating, memberid):
    users = await get_mentors()

    points = 5 * rating

    users[str(memberid)]["points"] += points

    if users[str(memberid)]["points"] > 50000:
        users[str(memberid)]["level"] = "Legend"
    elif users[str(memberid)]["points"] > 20000:
        users[str(memberid)]["level"] = "Platinum"
    elif users[str(memberid)]["points"] > 5000:
        users[str(memberid)]["level"] = "Gold"
    elif users[str(memberid)]["points"] > 2000:
        users[str(memberid)]["level"] = "Silver"
    elif users[str(memberid)]["points"] > 500:
        users[str(memberid)]["level"] = "Bronze"

    with open("mentors.json","w") as f:
        json.dump(users,f)

    return



#Find mentors function
async def find_available_mentors(subject,id):

    users = await get_mentors()

    def get_nth_key(dictionary, n=0):
        if n < 0:
            n += len(dictionary)
        for i, key in enumerate(dictionary.keys()):
            if i == n:
                return key
        raise IndexError("dictionary index out of range")

    mentors = []

    for i in range(len(users)):
        a = get_nth_key(users,i)
        if subject in users[str(a)]["subjects"] and users[str(a)]["activity"] == 1 and str(a) != str(id):
            mentors.append(int(a))

    return mentors

#Profile command
@client.command(aliases = ["profile","p"])
async def mentorProfile(ctx):
    users = await get_mentors()
    user=ctx.author

    blacklist = await get_blacklist()
    if str(ctx.author.id) in blacklist:
        await ctx.send("You have been blacklisted and therefore cannot use the bot's commands. Use $appeal to schedule an appeal.")
        return

    if str(user.id) not in users:
        await ctx.send('You are not registered as a mentor! Use "$registerAsMentor" to register.')
        return

    try:
        stats = users[str(ctx.author.id)]
    except:
        stats = []

    profile = discord.Embed(
        title = "{}'s mentor profile".format(ctx.author),
        colour = discord.Colour.blue()
    )
    profile.add_field(name="Points",value=stats["points"],inline=False)
    profile.add_field(name="Level",value=stats["level"],inline=False)
    if len(stats["subjects"]) == 0:
        profile.add_field(name="Subjects",value="None. Use $addSubject to add subjects!",inline=False)
    else:
        p = ""
        for i in stats["subjects"]:
            p += i + ", "
        profile.add_field(name="Subjects",value=p,inline=False)

    if stats["activity"] == 0:
        profile.add_field(name="Status",value="Inactive",inline=False)
    else:
        profile.add_field(name="Status",value="Active",inline=False)

    await ctx.send(embed = profile)





#Add subject command
@client.command(aliases=["adds","addmentorsubject","addSubjects"])
async def addSubject(ctx):

    blacklist = await get_blacklist()
    if str(ctx.author.id) in blacklist:
        await ctx.send("You have been blacklisted and therefore cannot use the bot's commands. Use $appeal to schedule an appeal.")
        return

    users = await get_mentors()

    if str(ctx.author.id) not in users:
        await ctx.send('You are not registered as a mentor! Use "$registerAsMentor" to register.')
        return

    subjects_lower=[]

    for i in range(len(subjects)):
        subjects_lower.append(subjects[i].lower())

    while (True):
        await ctx.send('Please input the subject you want! Type "Exit" to Exit')

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        message = await client.wait_for("message",check = check)

        if message.content.lower() == "exit":
            await ctx.send("Exited")
            return

        elif message.content.lower() in subjects_lower:

            subject = ""

            for i in range(len(subjects_lower)):
                if message.content.lower() == subjects_lower[i]:
                    subject = subjects[i]

            try:
                present = await add_subject(ctx.author, subject)
                if present == True:
                    await ctx.send("Added {}.".format(subject))
                else:
                    await ctx.send("You already have that subject!")
            except:
                await ctx.send("Something went wrong. If this persists, message ...Awkward#0252")

        else:
            await ctx.send("That is not a valid subject! If you think this is a mistake, please contact #...Awkward#0252.")




#Remove subject command
@client.command(aliases=["removes","removementorsubject","removeSubjects"])
async def removeSubject(ctx):

    blacklist = await get_blacklist()
    if str(ctx.author.id) in blacklist:
        await ctx.send("You have been blacklisted and therefore cannot use the bot's commands. Use $appeal to schedule an appeal.")
        return

    users = await get_mentors()

    if str(ctx.author.id) not in users:
        await ctx.send('You are not registered as a mentor! Use "$registerAsMentor" to register.')
        return

    if len(users[str(ctx.author.id)]["subjects"]) == 0:
        await ctx.send("You have no subjects to remove!")
        return

    subjects_lower=[]

    for i in range(len(subjects)):
        subjects_lower.append(subjects[i].lower())

    while (True):
        await ctx.send('Please input the subject you want to remove! Type "Exit" to Exit')

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        message = await client.wait_for("message",check = check)

        if message.content.lower() == "exit":
            await ctx.send("Exited")
            return

        elif message.content.lower() in subjects_lower:

            subject = ""

            for i in range(len(subjects_lower)):
                if message.content.lower() == subjects_lower[i]:
                    subject = subjects[i]

            try:
                present = await remove_subject(ctx.author, subject)
                if present == True:
                    await ctx.send("Removed {}.".format(subject))
                else:
                    await ctx.send("You don't have that subject!")
            except:
                await ctx.send("Something went wrong. If this persists, message ...Awkward#0252")

        else:
            await ctx.send("That is not a valid subject! If you think this is a mistake, please contact #...Awkward#0252.")




#Active/Inactive command
@client.command(aliases = ["activity","inactive","active","status"])
async def updateactivity(ctx):

    blacklist = await get_blacklist()
    if str(ctx.author.id) in blacklist:
        await ctx.send("You have been blacklisted and therefore cannot use the bot's commands. Use $appeal to schedule an appeal.")
        return


    users = await get_mentors()

    if str(ctx.author.id) not in users:
        await ctx.send('You are not registered as a mentor! Use "$registerAsMentor" to register.')
        return

    await update_activity(ctx.author)

    list = await get_mentors()
    activity = list[str(ctx.author.id)]["activity"]

    if activity == 1:
        await ctx.send("Activity set to `Active`")
    if activity == 0:
        await ctx.send("Activity set to `Inactive`")



#Can report questions and answers
@client.command(aliases = ["r"])
async def report(ctx):

    blacklist = await get_blacklist()
    if str(ctx.author.id) in blacklist:
        await ctx.send("You have been blacklisted and therefore cannot use the bot's commands. Use $appeal to schedule an appeal.")
        return

    messages = await get_messages()

    def check(m):
        if m.reference is not None:
            if str(m.reference.message_id) in messages:
                return messages[str(m.reference.message_id)]
        return 0

    reply = check(ctx.message)

    if reply == 0:
        await ctx.send("You can only report questions and answers!")
        return

    def check2(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send("Please state your reason.")

    reason = await client.wait_for("message",check = check2, timeout = 120)

    await ctx.send('Are you sure you want to submit this report? (Type "Yes" to submit. Type anything else to exit.)')

    def check3(message):
        return message.author == ctx.author and message.channel == ctx.channel

    submit = await client.wait_for("message",check = check3, timeout = 120)

    if submit.content.lower() == "yes":
        await reporting(reply, reason)
        await ctx.send("Reported")
    else:
        await ctx.send("Aborted")
        return



#Update Activity Function
async def update_activity(user):
    users = await get_mentors()

    users[str(user.id)]["activity"] = (users[str(user.id)]["activity"]+1)%2

    with open("mentors.json","w") as f:
        json.dump(users,f)

    return


#add subject function
async def add_subject(user,subject):
    users = await get_mentors()

    if subject in users[str(user.id)]["subjects"]:
        return False


    users[str(user.id)]["subjects"].append(subject)

    with open("mentors.json","w") as f:
        json.dump(users,f)

    return True


#remove subject function
async def remove_subject(user,subject):
    users = await get_mentors()

    if subject not in users[str(user.id)]["subjects"]:
        return False

    users[str(user.id)]["subjects"].remove(subject)

    with open("mentors.json","w") as f:
        json.dump(users,f)

    return True


#registration function
async def registration(user):
    users = await get_mentors()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["points"] = 0
        users[str(user.id)]["level"] = "Basic"
        users[str(user.id)]["subjects"] = []
        users[str(user.id)]["activity"] = 0

    with open("mentors.json","w") as f:
        json.dump(users,f)

    return True


#mentors function
async def get_mentors():
    with open("mentors.json","r") as f:
        users = json.load(f)

    return users

#increase counter
async def increase_counter():
    with open("counters.json","r") as f:
        messages = json.load(f)

    messages["messages"] += 1

    with open("counters.json","w") as f:
        json.dump(messages,f)

#log message (text):
async def log_message(user, message, id):
    with open("counters.json","r") as f:
        messages = json.load(f)

    log = open("logging.txt","a")
    if message.attachments:
        log.write("#{}, User: {}, Message: {}, Attachments: {} \n".format(messages["messages"], user.id, message.content, message.attachments[0].url))
    else:
        log.write("#{}, User: {}, Message: {} \n".format(messages["messages"], user.id, message.content))
    log.close()

    await log_json(user, message, id)

    await increase_counter()

#log message (json)
async def log_json(user, message, id):

    messageid = await get_messages()

    messageid[str(id.id)] = {}
    messageid[str(id.id)]["user"] = user.id
    messageid[str(id.id)]["message"] = message.content
    if message.attachments:
        messageid[str(message)]["attachments"] = message.attachments[0].url

    with open("messageid.json","w") as f:
        json.dump(messageid,f)

#get messages
async def get_messages():
    with open("messageid.json","r") as f:
        messages = json.load(f)

    return messages


#reports
async def reporting(message, reason):
    with open("counters.json","r") as f:
        reports = json.load(f)

    reportfile = open("reports.txt","a")
    try:
        reportfile.write("Report #{}, User: {}, Message: {}, Attachments: {}, Reason: {} \n".format(reports["reports"],message["user"],message["message"], message["attachments"], reason.content))
    except:
        reportfile.write("Report #{}, User: {}, Message: {}, Reason: {} \n".format(reports["reports"],message["user"],message["message"], reason.content))
    reportfile.close()

    reports["reports"] += 1

    with open("counters.json","w") as f:
        json.dump(reports,f)

    await report_user(message["user"])

#add user's name to badusers.json
async def report_user(user):

    with open("badusers.json","r") as f:
        users = json.load(f)

    if str(user) in users:
        users[str(user)]["infractions"] += 1
    else:
        users[str(user)] = {}
        users[str(user)]["infractions"] = 1

    if users[str(user)]["infractions"] >= 3:
        with open("blacklist.json","r") as g:
            blacklisted = json.load(g)

        blacklisted[str(user)] = {}

        with open("blacklist.json","w") as g:
            json.dump(blacklisted,g)

        mentors = await get_mentors()

        if str(user) in mentors:
            mentors[str(user)]["activity"] = 0

        with open("mentors.json","w") as h:
            json.dump(mentors,h)

    with open("badusers.json","w") as f:
        json.dump(users,f)

#get blacklist
async def get_blacklist():
    with open("blacklist.json","r") as f:
        blacklisted = json.load(f)

    return blacklisted


client.run("ODQ0MjIzNTU0ODYxNTMxMTc3.YKPSdA.AJgJUJA8rK_jQzX1omcIgpVikB0")
