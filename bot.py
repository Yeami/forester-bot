import os
import random

import discord

from discord.ext import commands
from db import _8ball_responses

client = commands.Bot(command_prefix='/')


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game('with Python [•w•] 24/7'),
    )
    print('I am ready!')


@client.event
async def on_member_join(member):
    print(f'The {member} has joined to the server!')


@client.event
async def on_member_remove(member):
    print(f'The {member} has left the server!')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(_8ball_responses)}')


@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'The user {member.mention} was banned!')


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for entry in banned_users:
        user = entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'The user {user.mention} was unbanned!')
            return


client.run(os.environ['BOT_TOKEN'])
