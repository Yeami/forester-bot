import discord
from discord.ext import commands, tasks
from discord.utils import get

import youtube_dl
import os
import random
from itertools import cycle

from db import _8ball_responses
from enums import RolesType
from utils import get_audio_length

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


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'[log] The bot has left from the {channel} channel')
        await ctx.send(f'Left from the **{channel}** channel')
    else:
        print('[log] Bot was told to leave voice channel, but was not in one')
        await ctx.send('Don`t think I am in a voice channel')


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Removed the old song file')
    except PermissionError:
        print('[log] Trying to delete song file, but it`s being played')
        await ctx.send('ERROR: Music is playing')
        return

    await ctx.send('Starting the preparations for playing an audio...')

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Downloading the audio...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'[log] Renamed the file name - {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print('[log] The audio is ready'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    audio_name = name.rsplit('-', 2)[0]
    length = get_audio_length('song.mp3')
    await ctx.send(f'Starting to play the audio\n**[{length}] {audio_name}**')
    print(f'[log] Starting to play the audio\n[{length}] {audio_name}')


@client.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print('[log] Audio was paused')
        voice.pause()
        await ctx.send('Audio was paused')
    else:
        print('[log] Audio is not playing, so pause was failed')
        await ctx.send('Audio is not playing, so pause was failed')


@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print('[log] Resumed the audio')
        voice.resume()
        await ctx.send('Resumed the audio')
    else:
        print('[log] Audio is not paused')
        await ctx.send('Audio is not paused')


@client.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print('[log] Audio was stopped')
        voice.stop()
        await ctx.send('Audio was stopped')
    else:
        print('[log] No audio is playing, so failed to stop')
        await ctx.send('No audio is playing, so failed to stop')


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
