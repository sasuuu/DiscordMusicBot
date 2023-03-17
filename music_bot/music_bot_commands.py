from discord.ext import commands
from searchers.youtube_video_searcher import *
from downloaders.youtube_downloader import *

LIST_LAST_ITEM_INDEX = -1

class MusicBotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play')
    async def play(self, ctx, *, message):
        if ctx.guild.id != self.bot.guild_id:
            print(f'Skipping because guild_id({ctx.guild.id}) is different than {self.bot.guild_id}')
            return
        
        voice_client = ctx.message.guild.voice_client
        if voice_client is None or not voice_client.is_connected():
            voice_client = await self.bot.add_bot_to_voice_channel(ctx)

        if voice_client is None:
            return
        
        if not message.startswith('https://'):
            youtube_link = search_for_video_link(message)
        else:
            youtube_link = message

        youtube_link_info = await get_info_from_url(youtube_link)

        if 'entires' in youtube_link_info:
            for entry in youtube_link_info['entries']:
                self.bot.songs.append({
                    'url': entry['url'],
                    'title': entry['title'],
                    'id': self.bot.songs[-1]['id'] + 1 if len(self.bot.songs) > 0 else 1
                })
            await ctx.send(f'{len(youtube_link_info["entries"])} songs from playlist added.')
        else:
            self.bot.songs.append({
                    'url': youtube_link_info['url'],
                    'title': youtube_link_info['title'],
                    'id': self.bot.songs[LIST_LAST_ITEM_INDEX]['id'] + 1 if len(self.bot.songs) > 0 else 1
                })
            await ctx.send(f'{youtube_link_info["title"]} added.')

        if voice_client is not None and not voice_client.is_playing():
            self.bot.play_next_song_from_queue()