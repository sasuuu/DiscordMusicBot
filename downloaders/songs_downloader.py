from time import sleep
from multiprocessing import Process, Event
from downloaders.youtube_downloader import *
import signal
import asyncio

NO_SONG_TO_DOWNLOAD_LOOP_DELAY = 5
MAX_PREDOWNLOADED_SONGS = 4

class SongsDownloader(Process):

    def __init__(self, songs_to_download, songs_to_download_lock, downloaded_songs, downloaded_songs_lock, download_in_progress, deamon=True):
        Process.__init__(self, daemon=deamon)
        self.songs_to_download = songs_to_download
        self.songs_to_download_lock = songs_to_download_lock
        self.downloaded_songs = downloaded_songs
        self.downloaded_songs_lock = downloaded_songs_lock
        self.stop_event = Event()
        self.download_in_progress = download_in_progress

    def get_next_song_to_download(self):
        self.songs_to_download_lock.acquire()
        try:
            next_song = self.songs_to_download.get_nowait()
        except:
            next_song = None
        finally:
            self.songs_to_download_lock.release()
        return next_song
    
    def put_downloaded_song_on_queue(self, downloaded_song_filename):
        self.downloaded_songs_lock.acquire()
        try:
            self.downloaded_songs.put(downloaded_song_filename)
        except:
            print(f'SongsDownloader(PID: {self.pid}): There was an error during putting downloaded song on queue')
        finally:
            self.downloaded_songs_lock.release()

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        print(f'SongsDownloader Process(PID: {self.pid}) started')
        while not self.stop_event.is_set():
            if self.downloaded_songs.qsize() >= MAX_PREDOWNLOADED_SONGS:
                sleep(NO_SONG_TO_DOWNLOAD_LOOP_DELAY)
                continue
            
            if self.songs_to_download.qsize() > 0:
                self.download_in_progress.set()

            song_to_download = self.get_next_song_to_download()
            if song_to_download is None:
                self.download_in_progress.clear()
                sleep(NO_SONG_TO_DOWNLOAD_LOOP_DELAY)
                continue

            downloaded_song_filename = asyncio.run(download_from_url(song_to_download))
            self.put_downloaded_song_on_queue(downloaded_song_filename)
            self.download_in_progress.clear()

        print(f'SongsDownloader Process(PID: {self.pid}) stopped')