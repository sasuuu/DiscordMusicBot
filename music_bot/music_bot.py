from discord.ext import commands
from players.music_player import *

TIME_BETWEEN_NEXT_CHECK_FOR_DOWNLOADED_SONG = 2

class MusicBot(commands.Bot):

    def __init__(self, prefix, guild_id):
        super().__init__(command_prefix=prefix)
        self.guild_id = int(guild_id)
        self.songs = []
        self.current_song_index = None

    async def add_bot_to_voice_channel(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(f'{ctx.message.author.name} is not connected to any voice channel')
            return None
        
        channel = ctx.message.author.voice.channel
        await channel.connect()
        self.songs = []
        self.current_song_index = None
        return ctx.message.guild.voice_client

    def play_next_song_from_queue(self, e=None):
        if e:
            print(f'Player error: {e}')

        voice_client = None
        for client in self.voice_clients:
            if client.guild.id == self.guild_id:
                voice_client = client

        if voice_client is None:
            print('Bot is not added to guild')
            return None
    
        if not voice_client.is_connected():
            print('Bot is not connected to any channel')
            return None
        
        if voice_client.is_playing():
            return None
        
        if self.current_song_index is None:
            self.current_song_index = 0
        else:
            self.current_song_index += 1

        if self.current_song_index >= len(self.songs):
            self.dispatch('disconnect_client', voice_client)
            return None

        player = get_player(self.songs[self.current_song_index]['url'])
        voice_client.play(player, after=self.play_next_song_from_queue)