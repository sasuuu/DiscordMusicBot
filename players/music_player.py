import discord
import pathlib

FFMPEG_PATH = '{}/executables/ffmpeg.exe'.format(pathlib.Path().resolve())
FFMPEG_OPTIONS = {
    'options': '-vn'
}

def get_player(filename, volume=0.5):
    return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename, executable=FFMPEG_PATH, **FFMPEG_OPTIONS), volume)