import discord
from discord.ext import commands
import os
import json
import random
client = commands.Bot(command_prefix = 'test! ')
client.remove_command('help')

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('test! help'))
  print('Bot is ready')

os.chdir("C:\\Users\\ethan\\Desktop\\Discord Bots\\Testing Bot")

mainshop = []

with open('shop.json') as f:
    data = json.load(f)

for name in data["mainshop"]:
    mainshop.append(name)

propertyshop = []

with open('property.json') as f:
    data = json.load(f)

for name in data["mainshop"]:
    propertyshop.append(name)

@client.command()
async def shop(ctx):
    embed = discord.Embed(
        title = "Shop",
        description = "Buy things here!",
        colour = discord.Colour.blurple()
    )

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        description = item["description"]
        embed.add_field(name = name, value = f"${price} | {description}")

    await ctx.send(embed = embed)

@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    embed = discord.Embed(
        title = f"{ctx.author}'s bag"
    )
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        embed.add_field(name = name, value = amount)

    await ctx.send(embed = embed)

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount
    users = await get_bank_data()
    bal = await update_bank(user)

    if bal[0] < cost:
        return[False,2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]

    with open("bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

@client.command(aliases=["properties"])
async def property(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        property = users[str(user.id)]["property"]
    except:
        property = []

    embed = discord.Embed(
        title = f"{ctx.author}'s properties"
    )
    for item in property:
        name = item["item"]
        amount = item["amount"]
        embed.add_field(name = name, value = amount)

    await ctx.send(embed = embed)


@client.command()
async def shopproperty(ctx):
    embed = discord.Embed(
        title = "Property Shop",
        description = "Buy properties here!",
        colour = discord.Colour.blurple()
    )

    for item in propertyshop:
        name = item["name"]
        price = item["price"]
        description = item["description"]
        embed.add_field(name = name, value = f"${price} | {description}")

    await ctx.send(embed = embed)

@client.command()
async def buyproperty(ctx, item, amount = 1):
    await open_account(ctx.author)

    res = await buy_property(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send("You don't have enough money to buy that!")
            return

    await ctx.send("You just bought {} {}".format(amount, item))

async def buy_property(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in propertyshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount
    users = await get_bank_data()
    bal = await update_bank(user)

    if bal[0] < cost:
        return[False,2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["property"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["property"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["property"] = [obj]

    with open("bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

@client.command(aliases = ["sellp"])
async def sellproperty(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_property(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("You cannot sell that item!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have that item!")
            return
        if res[1]==3:
            await ctx.send(f"You don't have that item!")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_property(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in propertyshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["property"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["property"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            return [False,3]
    except:
        return [False,3]

    with open("bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

@client.command()
async def buy(ctx, item, amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send("You don't have enough money to buy that!")
            return

    await ctx.send("You just bought {} {}".format(amount, item))

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("You cannot sell that item!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have that item!")
            return
        if res[1]==3:
            await ctx.send(f"You don't have that item!")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            return [False,3]
    except:
        return [False,3]

    with open("bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

@client.command()
async def balance(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(
        title = "{}'s balance".format(ctx.author.name),
        colour = discord.Colour.blurple()
    )
    embed.add_field(name = "Wallet Balance", value = wallet_amt)
    embed.add_field(name = "Bank Balance", value = bank_amt)
    await ctx.send(embed = embed)

@client.command()
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randint(0,100)

    await ctx.send("Someone gave you {}!".format(earnings))

    users[str(user.id)]["wallet"] += earnings

    with open("bank.json","w") as f:
        json.dump(users,f)

@client.command(aliases = ["dp"])
async def deposit(ctx,amount = None):

    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount you would like to deposit.")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send("You don't have enough money in your wallet to deposit!")
        return

    if amount<0:
        await ctx.send("Not a valid value.")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount, "bank")

    await ctx.send("You deposited ${}!".format(amount))

@client.command(aliases = ["wd"])
async def withdraw(ctx,amount = None):

    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount you would like to withdraw.")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send("You don't have enough money in the bank to withdraw!")
        return

    if amount<0:
        await ctx.send("Not a valid value.")
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount, "bank")

    await ctx.send("You withdrew ${}!".format(amount))


@client.command(aliases = ["give"])
async def send(ctx,member:discord.Member,amount = None):

    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("Please enter the amount you would like to give.")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send("You don't have enough money in your wallet to give!")
        return

    if amount<0:
        await ctx.send("Not a valid value.")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(member,amount)

    await ctx.send("You gave {} ${}!".format(member,amount))

@client.command()
async def slots(ctx,amount = 1):
    await open_account(ctx.author)

    if amount < 1:
        await ctx.send("Amount must be positive!")
        return

    users = await get_bank_data()

    user = ctx.author

    slots = [":dollar:", ":gem:",":coin:","<:wuh:834770605144277044>","<:weh:823640574874746960>"]

    slots1 = random.choice(slots)
    slots2 = random.choice(slots)
    slots3 = random.choice(slots)


    if (slots1 == slots2 and slots2 == slots3):
        if slots1 == "<:weh:823640574874746960>":
            await update_bank(ctx.author,50*amount)
            embed = discord.Embed(
                description = "{} rolled: {}{}{}. They won {}!".format(ctx.author,slots1,slots2,slots3,50*amount),
                colour = discord.Colour.blurple()
            )
            await ctx.send(embed=embed)
        else:
            await update_bank(ctx.author,20*amount)
            embed = discord.Embed(
                description = "{} rolled: {}{}{}. They won {}!".format(ctx.author,slots1,slots2,slots3,20*amount),
                colour = discord.Colour.blurple()
            )
            await ctx.send(embed=embed)
    elif (slots1 == slots2 or slots2 == slots3 or slots1 == slots3):
        await update_bank(ctx.author,amount*0)
        embed = discord.Embed(
            description = "{} rolled: {}{}{}. They won {}!".format(ctx.author,slots1,slots2,slots3,amount*0),
            colour = discord.Colour.blurple()
        )
        await ctx.send(embed=embed)
    else:
        await update_bank(ctx.author,-1*amount)
        embed = discord.Embed(
            description = "{} rolled: {}{}{}. They lost {}!".format(ctx.author,slots1,slots2,slots3,amount),
            colour = discord.Colour.blurple()
        )
        await ctx.send(embed=embed)

async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("bank.json","w") as f:
        json.dump(users,f)

    return True

async def get_bank_data():
    with open("bank.json","r") as f:
        users = json.load(f)

    return users

async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("bank.json", "w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)

    em = discord.Embed(title = f"Top {x} Richest People" ,
        description = "People with the most money in their bank and wallet:",
        colour = discord.Colour.blurple())
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

client.run("ODM1MjQwMDkzNDkyOTY5NDky.YIMj9A.ubxKL1lNWvNOqWudMvU-Xn-Furo")
