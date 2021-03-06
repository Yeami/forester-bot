import os

import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get

from enums import ColorsType
from utils import get_audio_length


class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.volume = 0.07
        # self.queues = {}

    @commands.command(pass_context=True, aliases=['j'])
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)
                print(f'[log] The bot has moved to the {channel} channel')
            else:
                await channel.connect()
                print(f'[log] The bot has connected to the {channel} channel')

            embed = discord.Embed(
                title=f'Joined to the {channel} channel',
                color=ColorsType.DEFAULT.value
            )
            embed.set_footer(
                text=f'Command used by {ctx.author.name}#{ctx.author.discriminator}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
        except AttributeError as e:
            embed = discord.Embed(
                title='Command error',
                description='I can`t connect to the channel because you have not connected to any one',
                color=ColorsType.ERROR.value
            )
            embed.set_footer(
                text=f'Command used by {ctx.author.name}#{ctx.author.discriminator}',
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)

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
        try:
            if os.path.isfile('song.mp3'):
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
            'quiet': True,
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('[log] Downloading the audio...')
            audio = ydl.extract_info(url=url, download=True)

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                print(f'[log] Renamed the file name - {file}')
                os.rename(file, 'song.mp3')

        voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print('[log] The audio is ready'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = self.volume

        audio_name = name.rsplit('-', 2)[0]
        length = get_audio_length('song.mp3')

        embed = discord.Embed(title=audio.get('title'), url=url, description='Now playing', color=ColorsType.DEFAULT.value)
        embed.add_field(name='Duration', value=length, inline=True)
        embed.add_field(name='Author', value=audio.get('uploader'), inline=True)
        embed.set_image(url=audio.get('thumbnail'))
        embed.set_footer(text=f'Command used by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
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
