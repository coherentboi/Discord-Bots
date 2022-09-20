import discord
from discord.ext import commands
import os
import random
from lists import nsfw_images
from lists import fuck_images
from lists import bj_images
from lists import fucks
from lists import bj

prefix = '!'

class nsfw(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Nsfw Cog is ready')

  @commands.command()
  async def nsfw(self, ctx):
    if ctx.channel.nsfw == False:
      await ctx.send("||Go here to see some NSFW images: <https://bit.ly/3v9grNg>||")
      return

    if os.getenv('nsfw') == '0':
      await ctx.send("The developer turned off NSFW commands.")
      return

    embed = discord.Embed(
      description = '{} used Nsfw'.format(ctx.author),
      colour = discord.Colour.red()
    )

    embed.set_footer(text='Nothing to see here...')
    embed.set_image(url = random.choice(nsfw_images))
    embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)

  @commands.command()
  async def fuck(self, ctx, person="them"):
    if ctx.channel.nsfw == False:
      await ctx.send("||Go here to see some NSFW images: <https://bit.ly/3v9grNg>||")
      return

    if os.getenv('nsfw') == '0':
      await ctx.send("The developer turned off NSFW commands.")
      return

    embed = discord.Embed(
      description = random.choice(fucks).format(ctx.author,person),
      colour = discord.Colour.red()
    )

    embed.set_footer(text='uhhhhhhh...ahhhhh...uhhhhhh...')
    embed.set_image(url = random.choice(fuck_images))
    embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)


  @commands.command(aliases=['hentai', 'nsfwRoulette'])
  async def nsfwRoll(self, ctx):
    if ctx.channel.nsfw == False:
      await ctx.send("||Go here to see some NSFW images: <https://bit.ly/3v9grNg>||")
      return

    if os.getenv('nsfw') == '0':
      await ctx.send("The developer turned off NSFW commands.")
      return

    a = random.randint(10000,360000)

    embed = discord.Embed(
      description = "Check out https://nhentai.net/g/{}".format(a),
      colour = discord.Colour.red()
    )

    embed.set_footer(text='Check it out!')
    embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)
    await ctx.send('https://nhentai.net/g/{}'.format(a))

  @commands.command(aliases=['bj'])
  async def blowjob(self, ctx, person=" "):
    if ctx.channel.nsfw == False:
      await ctx.send("||Go here to see some NSFW images: <https://bit.ly/3v9grNg>||")
      return

    if os.getenv('nsfw') == '0':
      await ctx.send("The developer turned off NSFW commands.")
      return

    embed = discord.Embed(
      description = random.choice(bj).format(ctx.author,person),
      colour = discord.Colour.red()
    )

    embed.set_footer(text='Slurpppppp')
    embed.set_image(url = random.choice(bj_images))
    embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(nsfw(client))
