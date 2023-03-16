from discord.ext import commands
from multiprocessing import Queue, Lock, Event
from downloaders.songs_downloader import *
from players.music_player import *
from time import sleep
import asyncio

TIME_BETWEEN_NEXT_CHECK_FOR_DOWNLOADED_SONG = 2

class MusicBot(commands.Bot):

    def __init__(self, prefix, guild_id):
        super().__init__(command_prefix=prefix)
        self.guild_id = int(guild_id)
        self.songs_to_download = Queue()
        self.songs_to_download_lock = Lock()
        self.downloaded_songs = Queue()
        self.downloaded_songs_lock = Lock()
        self.download_in_progress = Event()
        self.SongsDownloaderProcess = SongsDownloader(self.songs_to_download, self.songs_to_download_lock, self.downloaded_songs, self.downloaded_songs_lock, self.download_in_progress)
        print(f'Starting SongsDownloader Process')
        self.SongsDownloaderProcess.start()

    async def add_bot_to_voice_channel(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(f'{ctx.message.author.name} is not connected to any voice channel')
            return None
        
        channel = ctx.message.author.voice.channel
        await channel.connect()
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
        
        if self.songs_to_download.qsize() == 0 and self.downloaded_songs.qsize() == 0 and not self.download_in_progress.is_set():
            return None

        while True:
            next_song_to_play = self.get_song_from_downloaded_songs_queue()
            if next_song_to_play is not None:
                break
            sleep(TIME_BETWEEN_NEXT_CHECK_FOR_DOWNLOADED_SONG)

        player = get_player(next_song_to_play)
        voice_client.play(player, after=self.play_next_song_from_queue)

    def put_song_to_download_on_queue(self, song_to_download):
        self.songs_to_download_lock.acquire()
        try:
            self.songs_to_download.put(song_to_download)
        except:
            print('MusicBot: There was an error during putting song to download on queue')
        finally:
            self.songs_to_download_lock.release()

    def get_song_from_downloaded_songs_queue(self):
        self.downloaded_songs_lock.acquire()
        try:
            downloaded_song = self.downloaded_songs.get_nowait()
        except :
            downloaded_song = None
        finally:
            self.downloaded_songs_lock.release()

        return downloaded_song

    def finalize(self):
        print(f'Stopping SongsDownloader Process(PID: {self.SongsDownloaderProcess.pid})')
        self.SongsDownloaderProcess.stop_event.set()
        print(f'Waiting for SongsDownloader Process(PID: {self.SongsDownloaderProcess.pid}) exit')
        self.SongsDownloaderProcess.join()
        print(f'SongsDownloader Process exited with code {self.SongsDownloaderProcess.exitcode}')
        