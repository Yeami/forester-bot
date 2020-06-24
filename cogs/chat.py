import random

from discord.ext import commands

responses = [
    'It is certain.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes - definitely.',
    'You may rely on it.',
    'As I see it, yes.',
    'Most likely.',
    'Outlook good.',
    'Yes.',
    'Signs point to yes.',
    'Reply hazy, try again.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don`t count on it.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.'
]


class Chat(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'[log] The {member} has joined to the server!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'[log] The {member} has left from the server!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'> Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        await ctx.send(f'> Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(aliases=['delete', 'purge'], description='Deletes the [x] previous messages')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('> Please specify the number of messages to delete.')


def setup(client):
    client.add_cog(Chat(client))
