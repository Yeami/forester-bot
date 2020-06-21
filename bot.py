import os
import random

import discord

from discord.ext import commands
from db import _8ball_responses

client = commands.Bot(command_prefix='/')


@client.event
async def on_ready():
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


client.run(os.environ['BOT_TOKEN'])
