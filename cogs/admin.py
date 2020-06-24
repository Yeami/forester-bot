import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Kick the member from the server')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'> The user {member.mention} was kicked!')
        print(f'[log] The {member} was kicked from the server')

    @commands.command(description='Ban the member on the server')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'> The user {member.mention} was banned!')
        print(f'[log] The {member} was banned on the server')

    @commands.command(description='Unban the member on the server')
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for entry in banned_users:
            user = entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'> The user {user.mention} was unbanned!')
                print(f'[log] The {member} was unbanned on the server')
                return


def setup(client):
    client.add_cog(Admin(client))
