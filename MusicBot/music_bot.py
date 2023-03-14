from discord.ext import commands
from multiprocessing import Queue, Lock
from SongsDownloader.songs_downloader import *

class MusicBot(commands.Bot):

    def __init__(self, prefix, guild_id):
        super().__init__(command_prefix=prefix)
        self.guild_id = int(guild_id)
        self.songs_to_download = Queue()
        self.songs_to_download_lock = Lock()
        self.downloaded_songs = Queue()
        self.downloaded_songs_lock = Lock()
        self.SongsDownloaderProcess = SongsDownloader(self.songs_to_download, self.songs_to_download_lock, self.downloaded_songs, self.downloaded_songs_lock)
        print(f'Starting SongsDownloader Process')
        self.SongsDownloaderProcess.start()
        print(f'SongsDownloader Process started(PID: {self.SongsDownloaderProcess.pid})')

    def finalize(self):
        print(f'Stopping SongsDownloader Process(PID: {self.SongsDownloaderProcess.pid})')
        self.SongsDownloaderProcess.stop_event.set()
        print(f'Waiting for SongsDownloader Process(PID: {self.SongsDownloaderProcess.pid}) exit')
        self.SongsDownloaderProcess.join()
        print(f'SongsDownloader Process exited with code {self.SongsDownloaderProcess.exitcode}')
        