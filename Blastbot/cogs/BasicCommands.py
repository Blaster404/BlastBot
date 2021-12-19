import discord
import random
import asyncio
import aiohttp
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.flags import Intents
intents = discord.Intents.all()
intents.members = True
intents.messages = True

snipe_message_author = {}
snipe_message_content = {}

class BasicCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f':ping_pong: Pong! Latency is {round(self.client.latency * 1000)}ms')

    #Function can be named as _8ball
    @commands.command(aliases=['8ball', '8b'])
    async def eightball(self, ctx, *, question):
        responses = ['As I see it, yes.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     'Don’t count on it.',
                     'It is certain.',
                     'It is decidedly so.',
                     'Most likely.',
                     'My reply is no.',
                     'My sources say no.'
                     'Outlook not so good.',
                     'Outlook good.',
                     'Reply hazy, try again.'
                     'Signs point to yes.',
                     'Very doubtful.',
                     'Without a doubt.',
                     'Yes.',
                     'Yes definitely.',
                     'You may rely on it.']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    #Avatar Command
    @commands.command()
    async def avatar(self, ctx, member : discord.Member = None):
        if member ==  None:
            member = ctx.author
        
        memberAvatar = member.avatar_url
        
        avaEmbed = discord.Embed(title=f"{member.name}'s Avatar", color = discord.Colour.blurple())
        avaEmbed.set_image(url = memberAvatar)

        await ctx.send(embed = avaEmbed)

    @commands.Cog.listener()
    async def on_message(self, message):
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content
        await asyncio.sleep(60)
        del snipe_message_author[message.channel.id]
        del snipe_message_content[message.channel.id]

    #Snipe Command
    @commands.command()
    async def snipe(self, ctx):
        channel = ctx.channel
        try:
            snipeEmbed = discord.Embed(title=f'Last deleted message in #{channel.name}', description = snipe_message_content[channel.id], color = discord.Colour.orange())
            snipeEmbed.set_footer(text=f'Deleted by {snipe_message_author[channel.id]}')
            await ctx.send(embed = snipeEmbed)
        except:
            await ctx.send(f'There are no deleted messages in {channel.name}')

    #Cat command
    @commands.command(help = 'Shows a random cat picture')
    async def cat(self, ctx):
            response = requests.get('https://aws.random.cat/meow')
            data = response.json()
            embed = discord.Embed(
                title = 'Kitty Cat 🐈',
                description = 'Cats :star_struck:',
                colour = discord.Colour.purple()
                )
            embed.set_image(url=data['file'])            
            embed.set_footer(text="")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(BasicCommands(client))