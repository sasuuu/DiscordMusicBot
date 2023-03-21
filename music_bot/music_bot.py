from discord import Intents
from discord.ext import commands
from players.music_player import *

DICONNECT_MUSIC_BOT_EVENT = 'disconnect_client'

class MusicBot(commands.Bot):
    def __init__(self, prefix, guild_id):
        super().__init__(command_prefix=prefix, intents=Intents.all())
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
        
        self.current_song_index = 0 if self.current_song_index is None else self.current_song_index + 1

        if self.current_song_index >= len(self.songs):
            self.dispatch(DICONNECT_MUSIC_BOT_EVENT, voice_client)
            return None

        player = get_player(self.songs[self.current_song_index]['url'])
        voice_client.play(player, after=self.play_next_song_from_queue)

    def skip_song(self, voice_client):
        self.current_song_index = 0 if self.current_song_index is None else self.current_song_index + 1

        if self.current_song_index >= len(self.songs):
            self.dispatch(DICONNECT_MUSIC_BOT_EVENT, voice_client)
            return None

        voice_client.stop()
        player = get_player(self.songs[self.current_song_index]['url'])
        voice_client.play(player, after=self.play_next_song_from_queue)