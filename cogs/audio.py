import os

import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get

from utils import get_audio_length


class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases=['j'])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()
            print(f'[log] The bot has connected to the {channel} channel')

        await ctx.send(f'> Joined to the **{channel}** channel')

    @commands.command(pass_context=True, aliases=['l'])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f'[log] The bot has left from the {channel} channel')
            await ctx.send(f'> Left from the **{channel}** channel')
        else:
            print('[log] Bot was told to leave voice channel, but was not in one')
            await ctx.send('> Don`t think I am in a voice channel')

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, url: str):
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
                print('[log] Removed the old song file')
        except PermissionError:
            print('[log] Trying to delete song file, but it`s being played')
            await ctx.send('> ERROR: Music is playing')
            return

        await ctx.send('> Starting the preparations for playing an audio...')

        voice = get(self.client.voice_clients, guild=ctx.guild)

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
        await ctx.send(f'> Starting to play the audio\n**[{length}] {audio_name}**')
        print(f'[log] Starting to play the audio\n[{length}] {audio_name}')

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('[log] Audio was paused')
            voice.pause()
            await ctx.send('> Audio was paused')
        else:
            print('[log] Audio is not playing, so pause was failed')
            await ctx.send('> Audio is not playing, so pause was failed')

    @commands.command(pass_context=True, aliases=['r'])
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print('[log] Resumed the audio')
            voice.resume()
            await ctx.send('> Resumed the audio')
        else:
            print('[log] Audio is not paused')
            await ctx.send('> Audio is not paused')

    @commands.command(pass_context=True, aliases=['s'])
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('[log] Audio was stopped')
            voice.stop()
            await ctx.send('> Audio was stopped')
        else:
            print('[log] No audio is playing, so failed to stop')
            await ctx.send('> No audio is playing, so failed to stop')


def setup(client):
    client.add_cog(Audio(client))
