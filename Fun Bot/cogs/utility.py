import discord
from discord.ext import commands
from lists import eightball
import random

class utility(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Utility Cog is ready')

  @commands.command(aliases=['8ball'])
  async def _8ball(self,ctx,*,question=" "):
    if question == " ":
      await ctx.send("Please input a valid question.")
      return
    embed = discord.Embed(
      description = 'Question was: "{}". My answer is: "{}"'.format(question,random.choice(eightball)),
      colour = discord.Colour.green()
    )
    await ctx.send(embed = embed)

  @commands.command()
  async def suggest(self,ctx):
    embed = discord.Embed(
      description = "Go to this link to input suggestion: {}".format("https://forms.gle/mSNUH3skVD8e3R6A7"),
      colour = discord.Colour.green()
    )
    embed.set_footer(text = 'Thank you for the support! Fun bot is a community effort and needs your ideas!')
    await ctx.send(embed=embed)

  @commands.command()
  async def invite(self, ctx):
    embed = discord.Embed(
      description = "Thank you for inviting me! Go to this link to invite me to one of your servers: {}".format("https://discord.com/api/oauth2/authorize?client_id=830145837958955069&permissions=0&scope=bot"),
      colour = discord.Colour.green()
    )
    embed.set_footer(text = 'Thank you for inviting Fun Bot!')
    await ctx.send(embed=embed)

  @commands.command()
  async def avatar(self, ctx, member : discord.Member = None):
    if member == None:
      await ctx.send("Please specify whose avatar you'd like to see.")
      return
    await ctx.send('{}'.format(member.avatar_url))

  @commands.command()
  async def servericon(self, ctx):
      await ctx.send('{}'.format(ctx.guild.icon_url))

  @commands.command()
  async def membercount(self,ctx):
      await ctx.send('{}'.format(ctx.guild.member_count))

  @commands.command(aliases = ["msg"])
  async def dm(self, ctx, member:discord.Member=None,*, message = None):
    if (message == None):
      await ctx.send("You need to send a message.")
      return
    await member.send('{} tells you: {}'.format(ctx.author, message))
    await ctx.channel.purge(limit = 1)
    await ctx.send("Message sent")

def setup(client):
  client.add_cog(utility(client))
