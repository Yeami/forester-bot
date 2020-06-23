import discord
from discord.ext import commands, tasks
from discord.utils import get

import youtube_dl
import os
import random
from itertools import cycle

from db import _8ball_responses
from enums import RolesType

client = commands.Bot(command_prefix='/')
status = cycle(['with Python [•w•] 24/7', '( ͡° ͜ʖ ͡°)', '(ง ͡ʘ ͜ʖ ͡ʘ)ง'])


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game('with Python [•w•] 24/7'),
    )
    change_status.start()
    print(f'[log] {client.user.name} is ready!')


@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()
        print(f'[log] The bot has connected to the {channel} channel')

    await ctx.send(f'Joined to the **{channel}** channel')


@client.event
async def on_member_join(member):
    print(f'[log] The {member} has joined to the server!')


@client.event
async def on_member_remove(member):
    print(f'[log] The {member} has left the server!')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
@commands.has_role(RolesType.ADMINISTRATOR.value)
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(_8ball_responses)}')


@client.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the number of messages to delete.')


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
