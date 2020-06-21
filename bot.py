import os

import discord

from discord.ext import commands

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


client.run(os.environ['BOT_TOKEN'])
