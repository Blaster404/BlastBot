import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands.errors import BotMissingPermissions
from discord.flags import Intents
from typing import Optional 
intents = discord.Intents.all()
intents.members = True
intents.messages = True

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Clear command, if no arguments added after .clear, deletes 1 message by default
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, member: Optional[discord.Member], amount: int = 1):
        def _check(message):
            if member is None:
                return True
            else:
                if message.author != member:
                    return False
                _check.count += 1
                return _check.count <= amount
        _check.count = 0
        await ctx.channel.purge(limit=amount + 1 if member is None else 1000, check=_check)
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, you are missing the ``MANAGE_MESSAGES`` permission to use this command.')

    #Kick a member
    @commands.command()
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await ctx.send(f'Kicked {member.mention}')
        await member.kick(reason=reason)
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, you are missing the ``KICK_MEMBERS`` or ``BAN_MEMBERS`` permission or both.')

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please mention the user to kick.')

    #Ban a member
    @commands.command()
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await ctx.send(f'Banned {member.mention}')
        await member.ban(reason=reason)
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, you are missing the ``KICK_MEMBERS`` or ``BAN_MEMBERS`` permission or both.')

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please mention the user to ban.')

    #Unban a member
    @commands.command()
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
                return
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, you are missing the ``KICK_MEMBERS`` or ``BAN_MEMBERS`` permission or both.')

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please mention the user to unban.')

def setup(client):
    client.add_cog(Moderation(client))