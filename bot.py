import discord
from discord.ext import commands, tasks

import os
from itertools import cycle

client = commands.Bot(command_prefix='/')
extensions = [
    'cogs.admin',
    'cogs.audio',
    'cogs.chat',
]
status = cycle([
    'with Python [•w•] 24/7',
    '( ͡° ͜ʖ ͡°)',
    '(ง ͡ʘ ͜ʖ ͡ʘ)ง',
])

if __name__ == '__main__':
    for extension in extensions:
        client.load_extension(extension)


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game('with Python [•w•] 24/7'),
    )
    change_status.start()
    print(f'[log] {client.user.name} - {client.user.id} is ready | Library v{discord.__version__}')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


client.run(os.environ['BOT_TOKEN'], bot=True, reconnect=True)
