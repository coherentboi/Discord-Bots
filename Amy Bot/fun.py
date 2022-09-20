import discord
from discord.ext import commands
import random
from lists import insults
from lists import flirting
from lists import killing
from lists import quotes
from lists import vocabulary
from lists import slaps
from lists import bonk_list
from lists import simp_list

class fun(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Fun Cog is ready')

  @commands.command(aliases = ["hello", 'hey'])
  async def hi(self,ctx,*,person=" "):
    await ctx.send("Hello {}".format(ctx.author))

  @commands.command()
  async def quote(self,ctx):
    await ctx.send(quotes[random.randint(0,len(quotes))-1])

  @commands.command()
  async def weh(self,ctx):
    await ctx.send(vocabulary[random.randint(3,4)])

  @commands.command(aliases = ['vocab'])
  async def vocabulary(self,ctx):
    await ctx.send(random.choice(vocabulary))

  @commands.command()
  async def sigh(self,ctx):
    await ctx.send(vocabulary[random.randint(12,13)])

  @commands.command(aliases = ["nou"])
  async def no_u(self,ctx,):
    await ctx.send(vocabulary[random.randint(5,7)])

  @commands.command()
  async def wuh(self,ctx):
    await ctx.send(vocabulary[random.randint(22,23)])

  @commands.command()
  async def simpfor(self, ctx,*, person = "someone"):
      await ctx.send("{} is a simp for {} <:simp:823640309257863168>".format(ctx.author, person))

  @commands.command()
  async def simp(self, ctx,*,person = None):
      if person == None:
          await ctx.send("Who is a simp?")
          return
      embed = discord.Embed(
        description = person + " is a simp!",
        colour = discord.Colour.gold()
      )
      embed.set_image(url=random.choice(simp_list))
      try:
        await ctx.send(embed = embed)
      except:
        await ctx.send("Something went wrong.")

  @commands.command()
  async def slap(self,ctx,*,person=" "):
    if person == " ":
      await ctx.send("Please specify who to slap.")
      return
    embed = discord.Embed(
      description = random.choice(slaps).format(ctx.author,person),
      colour = discord.Colour.gold()
    )
    try:
      await ctx.send(embed = embed)
    except:
      await ctx.send("Something went wrong.")

  @commands.command(aliases=["bonk"])
  async def horny(self, ctx,*,person = "Bonk!"):
      embed = discord.Embed(
        description = person + " go to horny jail!",
        colour = discord.Colour.gold()
      )
      embed.set_image(url=random.choice(bonk_list))
      try:
        await ctx.send(embed = embed)
      except:
        await ctx.send("Something went wrong.")


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
