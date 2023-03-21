import discord

FFMPEG_OPTIONS = {
    'options': '-vn'
}

def get_player(filename, volume=0.5):
    return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), volume)