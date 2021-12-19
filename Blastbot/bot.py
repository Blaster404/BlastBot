import discord
import random
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.flags import Intents
intents = discord.Intents.all()
intents.members = True
intents.messages = True

#Prefix is set to .
client = commands.Bot(command_prefix = '.', intents = intents)

#Event
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Haha blast blast go brr brr'))
    print(f'{client.user.name} is online.')

#Owner's id of the bot, this is used for loading cog files whereas regular server admins and members do not have access to.
def owner(ctx):
    return ctx.author.id == 'Your discord id, remove the apostrophe and paste your user id'

#Load cogs
@client.command()
@commands.check(owner)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Loaded cog.')
@load.error
async def load_error(ctx, error):
    await ctx.send('You are not the owner to be able to execute this command.')

#Unload cogs
@client.command()
@commands.check(owner)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('Unloaded cog.')
@unload.error
async def unload_error(ctx, error):
    await ctx.send('You are not the owner to be able to execute this command.')

#Reload cogs
@client.command()
@commands.check(owner)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Reloaded cog.')
@reload.error
async def reload_error(ctx, error):
    await ctx.send('You are not the owner to be able to execute this command.')

#Locate folder and checks if folder content files ends with .py
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#HELP COMMAND
funcommands = '''.8ball simply do .8ball <yourquestion> to for the 8ball to dictate your outcome.\n
    .ping Ping the latency of the bot.\n
    .avatar <user> gives the avatar of the user\n
    .snipe shows the last deleted message the last 60 seconds\n
    .cat Shows a random cat picture
    '''

moderationcommands = '''.clear <value> to clear the amount of messages\n
    .clear <member> <value> to clear the amount of messages last send by the user.\n
    .kick <member> <reason> to kick a member\n
    .ban <member> <reason> to ban a member\n
    .unban exampleuser#0000 to unban a member
    '''

client.remove_command("help")
@client.group(invoke_without_command=True)
async def help(ctx):
    HelpEmbed = discord.Embed(title = 'List of commands', description = 'List of commands.', color = discord.Colour.red())
    HelpEmbed.add_field(name='Fun commands', value=funcommands, inline=True)
    HelpEmbed.add_field(name='Moderation Commands', value=moderationcommands, inline=True)
    HelpEmbed.set_footer(text=f'{client.user.name} is still in developement.')
    await ctx.send(embed=HelpEmbed)

#Token
client.run('PASTE YOUR BOT TOKEN HERE')