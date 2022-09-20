import discord
from discord.ext import commands
import random
from lists import insults
from lists import flirting
from lists import killing

class fun(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Fun Cog is ready')

  @commands.command(aliases = ["hello", 'hey'])
  async def hi(self,ctx):
    await ctx.send("Hello {}".format(ctx.author))

  @commands.command(aliases = ['roast'])
  async def bully(self,ctx,*,person=" "):
    if person == " ":
      await ctx.send("Please specify who to bully.")
      return
    embed = discord.Embed(
      description = random.choice(insults).format(person),
      colour = discord.Colour.gold()
    )
    try:
      await ctx.send(embed = embed)
    except:
      await ctx.send("Something went wrong.")

  @commands.command()
  async def flirt(self,ctx,*,person=" "):
    if person == " ":
      await ctx.send("Please specify who to flirt with.")
      return
    if str(ctx.author.id) in person:
      await ctx.send("Imagine flirting with yourself. I can't believe you are that lonely.")
      return
    embed = discord.Embed(
      description = random.choice(flirting).format(person),
      colour = discord.Colour.gold()
    )
    try:
      await ctx.send(embed = embed)
    except:
      await ctx.send("Something went wrong.")

  @commands.command()
  async def kill(self,ctx,*,person=" "):
    if person == " ":
      await ctx.send("Please specify who to kill.")
      return
    if str(ctx.author.id) in person:
      await ctx.send("Noooo!!! Don't do that!!! You have a lot to live for!")
      return
    embed = discord.Embed(
      description = random.choice(killing).format(person),
      colour = discord.Colour.gold()
    )
    try:
      await ctx.send(embed = embed)
    except:
      await ctx.send("Something went wrong.")

  @commands.command()
  async def roll(self, ctx,*,size="6"):
    embed = discord.Embed(
      description = ":game_die: {} rolled a {} sided die and got a {}".format(ctx.author,size,random.randint(1,int(size))),
      colour = discord.Colour.gold()
    )
    try:
      await ctx.send(embed = embed)
    except:
      await ctx.send("Something went wrong.")


def setup(client):
  client.add_cog(fun(client))
