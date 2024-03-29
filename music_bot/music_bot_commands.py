from discord.ext import commands
from searchers.youtube_video_searcher import *
from downloaders.youtube_downloader import *

LIST_LAST_ITEM_INDEX = -1
ENTRIES_KEY = 'entries'

class MusicBotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, message):
        if ctx.guild.id != self.bot.guild_id:
            print(f'Skipping because guild_id({ctx.guild.id}) is different than {self.bot.guild_id}')
            return
        
        youtube_link = search_for_video_link(message) if not message.startswith('https://') else message

        youtube_link_info = await get_info_from_url(youtube_link, loop=self.bot.loop)

        if youtube_link_info is None:
            await ctx.send(f'Invalid youtube link')
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client is None or not voice_client.is_connected():
            voice_client = await self.bot.add_bot_to_voice_channel(ctx)

        if ENTRIES_KEY in youtube_link_info:
            for entry in youtube_link_info[ENTRIES_KEY]:
                self.bot.songs.append({
                    'url': entry['url'],
                    'title': entry['title'],
                    'id': self.bot.songs[LIST_LAST_ITEM_INDEX]['id'] + 1 if len(self.bot.songs) > 0 else 1
                })
            await ctx.send(f'{len(youtube_link_info[ENTRIES_KEY])} songs from playlist added.')
        else:
            self.bot.songs.append({
                    'url': youtube_link_info['url'],
                    'title': youtube_link_info['title'],
                    'id': self.bot.songs[LIST_LAST_ITEM_INDEX]['id'] + 1 if len(self.bot.songs) > 0 else 1
                })
            await ctx.send(f'{youtube_link_info["title"]} added.')

        if voice_client is not None and not voice_client.is_playing():
            self.bot.play_next_song_from_queue()
    
    @commands.command()
    async def skip(self, ctx):
        if ctx.guild.id != self.bot.guild_id:
            print(f'Skipping because guild_id({ctx.guild.id}) is different than {self.bot.guild_id}')
            return
        
        voice_client = ctx.message.guild.voice_client
        if voice_client is None or not voice_client.is_connected():
            await ctx.send('Bot is not connected to any channel')

        self.bot.skip_song(voice_client)

        
