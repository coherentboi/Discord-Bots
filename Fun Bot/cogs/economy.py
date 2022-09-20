import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from discord.ext.commands import CommandOnCooldown
import json
import random
import os



mainshop = []

with open('cogs\\shop.json') as f:
    data = json.load(f)

for name in data["mainshop"]:
    mainshop.append(name)

class economy(commands.Cog):

    def __init__(self, client):
            self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print('Economy Cog is ready')

    os.chdir("C:\\Users\\ethan\\Desktop\\Discord Bots\\Fun Bot")

    @commands.command(aliases=["bal"])
    async def balance(self,ctx):
        await open_account(ctx.author)

        user = ctx.author
        users = await get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        embed = discord.Embed(
            title = "{}'s balance".format(ctx.author.name),
            colour = discord.Colour.blurple()
            )
        embed.add_field(name = "Wallet Balance", value = "{} Fun Coins".format(wallet_amt))
        embed.add_field(name = "Bank Balance", value = "{} Fun Coins".format(bank_amt))
        await ctx.send(embed = embed)

    @commands.command()
    @commands.cooldown(1,10,BucketType.user)
    async def beg(self,ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings = random.randint(1,25)

        await ctx.send("Someone gave you {} Fun Coins!".format(earnings))

        users[str(user.id)]["wallet"] += earnings

        with open("cogs\\bank.json","w") as f:
            json.dump(users,f)

    @commands.command()
    @commands.cooldown(1,86400,BucketType.user)
    async def daily(self,ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings = random.randint(100,500)

        await ctx.send("Your daily reward is {} Fun Coins!".format(earnings))

        users[str(user.id)]["wallet"] += earnings

        with open("cogs\\bank.json","w") as f:
            json.dump(users,f)

    @commands.command(aliases = ["dp"])
    async def deposit(self,ctx,amount = None):

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

        await ctx.send("You deposited {} Fun Coins!".format(amount))

    @commands.command(aliases = ["wd"])
    async def withdraw(self,ctx,amount = None):

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

        await ctx.send("You withdrew {} Fun Coins!".format(amount))

    @commands.command(aliases = ["give"])
    async def send(self,ctx,member:discord.Member,amount = None):

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

        await ctx.send("You gave {} {} Fun Coins!".format(member,amount))

    @commands.command(aliases = ["gamble"])
    @commands.cooldown(1,20,BucketType.user)
    async def slots(self,ctx,amount = 1):
        await open_account(ctx.author)

        if ctx.channel.id == 767834437274435625:
            return
        if ctx.channel.id == 765675321949028413:
            return

        bal = await update_bank(ctx.author)

        if amount > bal[0]:
            await ctx.send("You don't have enough money in your wallet to gamble!")
            return

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
                    description = "{} rolled: {}{}{}. They won {} Fun Coins!".format(ctx.author,slots1,slots2,slots3,50*amount),
                    colour = discord.Colour.blurple()
                )
                await ctx.send(embed=embed)
            else:
                await update_bank(ctx.author,20*amount)
                embed = discord.Embed(
                    description = "{} rolled: {}{}{}. They won {} Fun Coins!".format(ctx.author,slots1,slots2,slots3,20*amount),
                    colour = discord.Colour.blurple()
                )
                await ctx.send(embed=embed)
        else:
            await update_bank(ctx.author,-1*amount)
            embed = discord.Embed(
                description = "{} rolled: {}{}{}. They lost {} Fun Coins!".format(ctx.author,slots1,slots2,slots3,amount),
                colour = discord.Colour.blurple()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def shop(self,ctx):
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

        embed.set_footer(text = "These are the season 1 items available for purchase on Fun Bot. Shop resets 5/31/2021")

        await ctx.send(embed = embed)

    @commands.command(aliases = ["inv","inventory"])
    async def bag(self,ctx):
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

    @commands.command()
    async def buy(self, ctx,*, item,):
        amount = 1
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


    @commands.command()
    async def sell(self,ctx,*,item,amount = 1):
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

    @commands.Cog.listener()
    async def on_command_error(self,ctx,exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send("That command is on cooldown for another {} seconds".format(round(exc.retry_after,2)))







#Non Discord Functions

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

    with open("cogs\\bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("cogs\\bank.json","w") as f:
        json.dump(users,f)

    return True

async def get_bank_data():
    with open("cogs\\bank.json","r") as f:
        users = json.load(f)

    return users

async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("cogs\\bank.json", "w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

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

    with open("cogs\\bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

def setup(client):
  client.add_cog(economy(client))
