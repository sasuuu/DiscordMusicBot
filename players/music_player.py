import discord

FFMPEG_OPTIONS = {
    'options': '-vn'
}
BEFORE_OPTIONS = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

def get_player(filename, volume=0.5):
    return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename, before_options=BEFORE_OPTIONS, **FFMPEG_OPTIONS), volume)