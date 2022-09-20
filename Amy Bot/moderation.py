import discord
from discord.ext import commands
import time

class moderation(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Moderation Cog is ready')

  @commands.command()
  async def kick(self, ctx, member : discord.Member=None,*, reason=None):
    if ctx.author.guild_permissions.kick_members == False:
      await ctx.send("Insufficient Permissions")
      return

    if member==None:
      await ctx.send("Please specify who to kick.")
      return

    roles = ctx.author.roles
    roles.reverse()
    author_top_role = roles[0]

    roles = member.roles
    roles.reverse()
    remove_member_top_role = roles[0]

    if (author_top_role <= remove_member_top_role):
      await ctx.send("Insufficient Permissions")
      return

    try:
      await member.kick(reason=reason)
      await member.send("You were kicked from '{}' for reason '{}'".format(ctx.guild.name, reason))
    except:
      await ctx.send("Something went wrong.")

  @commands.command()
  async def ban(self, ctx, member : discord.Member=None,*, reason=None):
    if ctx.author.guild_permissions.ban_members == False:
      await ctx.send("Insufficient Permissions")
      return

    if member==None:
      await ctx.send("Please specify who to ban.")
      return

    roles = ctx.author.roles
    roles.reverse()
    author_top_role = roles[0]

    roles = member.roles
    roles.reverse()
    remove_member_top_role = roles[0]

    if (author_top_role <= remove_member_top_role):
      await ctx.send("Insufficient Permissions")
      return

    try:
      await member.ban(reason=reason)
      await member.send("You were banned from '{}' for reason '{}'".format(ctx.guild.name, reason))
    except:
      await ctx.send("Something went wrong.")

  @commands.command()
  async def unban(self, ctx,*,member=""):
    if member ==  "":
      await ctx.send("Please specify a member to unban.")
      return

    if ctx.author.guild_permissions.ban_members == False:
      await ctx.send("Insufficient Permissions")
      return

    banned_users = await ctx.guild.bans()
    member_name,member_discriminator=member.split('#')

    for ban_entry in banned_users:
      user = ban_entry.user

      if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send('Unbanned {}#{}'.format(user.name, user.discriminator))

  @commands.command(aliases=['shutup'])
  async def mute(self, ctx, member:discord.Member=None,*, reason = None):
    if ctx.author.guild_permissions.manage_roles == False:
      await ctx.send("Insufficient Permissions")
      return

    if member==None:
      await ctx.send("Please specify who to mute.")
      return

    roles = ctx.author.roles
    roles.reverse()
    author_top_role = roles[0]

    roles = member.roles
    roles.reverse()
    remove_member_top_role = roles[0]

    if (author_top_role <= remove_member_top_role):
      await ctx.send("Insufficient Permissions")
      return

    role = discord.utils.get(ctx.guild.roles, name="Muted")
    try:
      await member.add_roles(role)
      await ctx.send(f'Muted {member.mention}')
      await member.send("You were muted in '{}' for reason '{}'".format(ctx.guild.name, reason))
    except:
      await ctx.send("Something went wrong.")


  @commands.command()
  async def cancel(self, ctx, member:discord.Member=None):
    if ctx.author.guild_permissions.manage_roles == False:
      await ctx.send("Insufficient Permissions")
      return

    if member==None:
      await ctx.send("Please specify who to cancel.")
      return

    roles = ctx.author.roles
    roles.reverse()
    author_top_role = roles[0]

    roles = member.roles
    roles.reverse()
    remove_member_top_role = roles[0]

    if (author_top_role <= remove_member_top_role):
      await ctx.send("Insufficient Permissions")
      return

    role = discord.utils.get(ctx.guild.roles, name="Cancelled")
    try:
      await member.add_roles(role)
      await ctx.send(f'Cancelled {member.mention}')
    except:
      await ctx.send("Something went wrong.")


  @commands.command()
  async def unmute(self, ctx, member: discord.Member=None):
    if ctx.author.guild_permissions.manage_roles == False:
      await ctx.send("Insufficient Permissions")

    roles = ctx.author.roles
    roles.reverse()
    author_top_role = roles[0]

    roles = member.roles
    roles.reverse()
    remove_member_top_role = roles[0]

    if (author_top_role <= remove_member_top_role):
      await ctx.send("Insufficient Permissions")
      return

    role = discord.utils.get(ctx.guild.roles, name="Muted")
    try:
      await member.remove_roles(role)
      await ctx.send(f'Unmuted {member.mention}')
    except:
      await ctx.send("Member was not Muted")

  @commands.command()
  async def absolutePowerKick(self,ctx,member:discord.Member=None,*, reason = None):
    if ctx.author.id != 634529260324782089:
      return
    await member.kick(reason=reason)

  @commands.command()
  async def absolutePowerBan(self,ctx,member:discord.Member=None,*, reason = None):
    if ctx.author.id != 634529260324782089:
      return
    await member.ban(reason=reason)

  @commands.command()
  async def absolutePowerMute(self,ctx,member:discord.Member=None,*, reason = None):
    if ctx.author.id != 634529260324782089:
      return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)

  @commands.command()
  async def clear(self,ctx, messages : int = 0):
    if ctx.author.guild_permissions.manage_messages == False:
      await ctx.send('Insufficient Permissions')
      return
    await ctx.channel.purge(limit=messages+1)
    message = await ctx.send('{} messages cleared.'.format(messages))
    time.sleep(1)
    await ctx.channel.purge(limit = 1)

def setup(client):
  client.add_cog(moderation(client))
