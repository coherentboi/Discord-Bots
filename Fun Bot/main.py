import discord
from discord.ext import commands
import os
from lists import helpcommands
from lists import credit
client = commands.Bot(command_prefix = '!', case_insensitive=True)
client.remove_command('help')

os.chdir("C:\\Users\\ethan\\Desktop\\Discord Bots\\Fun Bot")

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('!help'))
  print('Bot is ready')

@client.command()
async def unload(ctx,extension):
  client.unload_extension(f'cogs.{extension}')

@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = 'Fun Bot Help',
    description = '{} used !help.'.format(ctx.author),
    colour = discord.Colour.blue()
  )

  embed.set_footer(text='Message ...Awkward#0252 if something is not working.')
  embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
  for name, value, inline in helpcommands:
    embed.add_field(name=name, value=value, inline=inline)
  await ctx.send(embed=embed)

@client.command()
async def credits(ctx):
  embed = discord.Embed(
    title = 'Fun Bot Credits',
    description = 'Thank you to all these people:',
    colour = discord.Colour.blue()
  )
  for name, value, inline in credit:
    embed.add_field(name= await client.fetch_user(name), value=value, inline=inline)
  embed.add_field(name = "You guys!", value = "For helping support and develop Fun Bot", inline = False)
  await ctx.send(embed=embed)

@client.command()
async def servers(ctx):
  activeservers = client.guilds
  for guild in activeservers:
    print(guild.name)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

client.run("ODMwMTQ1ODM3OTU4OTU1MDY5.YHCbjw.hBw-CCstMNwZzgvePY6qjg2y83o")
