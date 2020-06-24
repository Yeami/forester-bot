import discord
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['delete', 'purge'], description='Deletes the [x] previous messages')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('> Please specify the number of messages to delete.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'[log] The {member} has joined to the server!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'[log] The {member} has left from the server!')


def setup(client):
    client.add_cog(Chat(client))
