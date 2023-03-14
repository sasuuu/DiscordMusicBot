from time import sleep
from multiprocessing import Process, Event
import signal

class SongsDownloader(Process):

    def __init__(self, songs_to_download, songs_to_download_lock, downloaded_songs, downloaded_songs_lock, deamon=True):
        Process.__init__(self, daemon=deamon)
        self.songs_to_download = songs_to_download
        self.songs_to_download_lock = songs_to_download_lock
        self.downloaded_songs = downloaded_songs
        self.downloaded_songs_lock = downloaded_songs_lock
        self.stop_event = Event()

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        while not self.stop_event.is_set():
            sleep(5)
            print(f'Process with name: {self.name} is working')

        print(f'Process({self.name}) stopped')