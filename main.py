import pathlib
import asyncio
import platform
from music_bot.music_bot import *
from configuration.configuration import *
from searchers.youtube_video_searcher import *
from downloaders.youtube_downloader import *

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

CONFIG_FILE = '{}/config.json'.format(pathlib.Path(__file__).parent.resolve())
CONFIGURATION = read_configuration(CONFIG_FILE)
DISCORD_TOKEN = CONFIGURATION["discord_token"]
DISCORD_GUID_ID = CONFIGURATION["discord_guild_id"]
DISCORD_COMMAND_PREFIX = "!"

if __name__ == "__main__":
    print(f'Discord token: {DISCORD_TOKEN}')
    print(f'Discord guild: {DISCORD_GUID_ID}')
    bot = MusicBot(DISCORD_COMMAND_PREFIX, DISCORD_GUID_ID)

    @bot.command(name='play')
    async def play(ctx, *, message):
        if ctx.guild.id != ctx.bot.guild_id:
            print(f'Skipping because guild_id({ctx.guild.id}) is different than {ctx.bot.guild_id}')
            return
        
        voice_client = ctx.message.guild.voice_client
        if voice_client is None or not voice_client.is_connected():
            voice_client = await ctx.bot.add_bot_to_voice_channel(ctx)

        if voice_client is None:
            return
        
        if not message.startswith('https://'):
            youtube_link = search_for_video_link(message)
        else:
            youtube_link = message

        youtube_link_info = await get_info_from_url(youtube_link)

        if 'entires' in youtube_link_info:
            for entry in youtube_link_info['entries']:
                ctx.bot.songs.append({
                    'url': entry['url'],
                    'title': entry['title'],
                    'id': ctx.bot.songs[-1]['id'] + 1 if len(ctx.bot.songs) > 0 else 1
                })
            await ctx.send(f'{len(youtube_link_info["entries"])} songs from playlist added.')
        else:
            ctx.bot.songs.append({
                    'url': youtube_link_info['url'],
                    'title': youtube_link_info['title'],
                    'id': ctx.bot.songs[-1]['id'] + 1 if len(ctx.bot.songs) > 0 else 1
                })
            await ctx.send(f'{youtube_link_info["title"]} added.')

        if voice_client is not None and not voice_client.is_playing():
            ctx.bot.play_next_song_from_queue()

    @bot.event
    async def on_ready():
        print("Logged in as a bot {0.user}".format(bot))

    bot.run(DISCORD_TOKEN)