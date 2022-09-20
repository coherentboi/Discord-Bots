import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from discord.ext.commands import CommandOnCooldown
import os
from lists import helpcommands
from lists import credit
import json
client = commands.Bot(command_prefix = '!amy ')
client.remove_command('help')

#on ready
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('!amy help'))
  print('Bot is ready')

@client.command()
async def update(ctx):
  user = await client.fetch_user(546499804964847642) #This is amy's id
  if (ctx.author.id != 634529260324782089): #This is mine
    ctx.send("This command is reserved for devs.")
    return

  filename = "amyavatar.png"
  await user.avatar_url.save(filename)
  with open("amyavatar.png", "rb") as file:
     await client.user.edit(avatar=file)


#Access the help menu
@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = 'Amy Bot Help',
    description = '{} used !amy help.'.format(ctx.author),
    colour = discord.Colour.blue()
  )

  embed.set_footer(text='Message ...Awkward#0252 or NeoTytanX#8468 if something is not working.')
  embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
  for name, value, inline in helpcommands:
    embed.add_field(name=name, value=value, inline=inline)
  await ctx.send(embed=embed)


#access credits page
@client.command()
async def credits(ctx):
  embed = discord.Embed(
    title = 'Amy Bot Credits',
    description = 'Thank you to all these people:',
    colour = discord.Colour.blue()
  )
  for name, value, inline in credit:
    embed.add_field(name= await client.fetch_user(name), value=value, inline=inline)
  embed.add_field(name = "You guys!", value = "For helping support and develop Amy Bot", inline = False)
  await ctx.send(embed=embed)


#see which servers (serverside only)
@client.command()
async def servers(ctx):
  activeservers = client.guilds
  for guild in activeservers:
    print(guild.name)

#catches errors
@client.event
async def on_command_error(ctx,exc):
    if isinstance(exc, CommandOnCooldown):
        await ctx.send("That command is on cooldown for another {} seconds".format(round(exc.retry_after,2)))
    else:
        await ctx.send('That command does not exist! Did you check for spelling? Use the command "!amy help" to find a list of commands!')


#Unloads cogs
client.load_extension("economy")
client.load_extension("fun")
client.load_extension("moderation")
client.load_extension("nsfw")
client.load_extension("utility")


#run command
client.run("ODMwMTAyMjUzMzM5MDE3Mjk2.YHBy9w.2kfVk-Vkes9sou95L16OH7PlK5E")
