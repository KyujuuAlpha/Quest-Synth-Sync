from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.clock import mainthread
from kivy.properties import NumericProperty
from android.permissions import Permission, request_permissions

import sync
import threading
import math
import time

# thread constants
DOWNLOAD_THREAD_COUNT = 6
THREAD_SPAWN_DELAY = 0.2

# main root widget
class MainScreen(MDScreen):

    # counters for status updates
    download_counter = 0
    download_max = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlist.text = sync.load_playlists()

    @mainthread
    def set_in_progress(self, disabled):
        # lock the ui according to the disabled parameter
        self.playlist.disabled = disabled
        self.exit_button.disabled = disabled
        self.button.disabled = disabled
        self.spinner.active = disabled
    
    @mainthread
    def set_status_text(self, text):
        # set the status of the downloading
        self.status.text = text

    @mainthread
    def status_counter_increase(self):
        self.download_counter += 1
        self.status.text = "Downloaded " + str(self.download_counter) + " of " + str(self.download_max)
    
    @mainthread
    def status_counter_reset(self, max):
        self.download_counter = 0
        self.download_max = max
        self.status.text = "Downloaded " + str(self.download_counter) + " of " + str(self.download_max)
    
    def song_download_worker(self, songs):
        for song in songs:
            sync.download_song(song)
            self.status_counter_increase()

    def download_thread(self):
        # split for multiple playlist support
        playlists = self.playlist.text.split(",")

        # loop for multiple playlists
        for playlist in playlists:
            # retrieve playlist
            playlist_id = playlist.strip()

            # make sure it's a real user and not blank
            if len(playlist_id) == 0:
                continue

            # retrieve songs from SynthRiderz
            self.set_status_text("Retrieving downloads for " + playlist_id)

            # retrieve songs from bsaber for the current page
            playlist_name, songs = sync.get_sr_songs(playlist_id)
            num_songs = len(songs)

            # if there are songs, then download and extract them
            if songs != None and num_songs > 0:
                threads = []
                self.status_counter_reset(num_songs)

                # if there are more dongs than the thread count, then split it up
                if num_songs >= DOWNLOAD_THREAD_COUNT:
                    chunk_size = math.floor(num_songs / DOWNLOAD_THREAD_COUNT)
                    for i in range(0, DOWNLOAD_THREAD_COUNT):
                        worker_song_list = []
                        if i == DOWNLOAD_THREAD_COUNT - 1:
                            worker_song_list = songs[(chunk_size * i):] # assign remaining songs to last worker
                        else: 
                            worker_song_list = songs[(chunk_size * i):(chunk_size * (i + 1))] # extract chunk of songs for each worker
                        threads.append(threading.Thread(target = (self.song_download_worker), args=[worker_song_list]))
                        threads[-1].start()
                        time.sleep(THREAD_SPAWN_DELAY)
                else:
                    # if not, just assign all songs to one thread
                    threads.append(threading.Thread(target = (self.song_download_worker), args=[songs]))
                    threads[-1].start()
                
                # wait for workers to finish
                for thread in threads:
                    thread.join()
            else:
                self.set_status_text(playlist_id + " has no songs!")
                time.sleep(3)

            # create playlist for this playlist
            sync.create_playlist(playlist_id, playlist_name)

        # done sync
        self.set_status_text("Songs synchronized!")
        self.set_in_progress(False)

    # called when the synchronize button is pressed
    def sync(self):
        if len(self.playlist.text) == 0:
            self.set_status_text("Please enter playlist ID!")
            return
        
        # check if path exists
        sync.safe_path_check()

        # save user input
        sync.save_playlists(self.playlist.text)
        
        # lock the buttons and start the master download thread
        self.set_in_progress(True)
        threading.Thread(target = (self.download_thread)).start()

    # called when the exit button is pressed
    def exit(self):
        exit()

# the main application construction
class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return MainScreen()

if __name__ == "__main__":
    # make sure permissions are satisfied
    request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    # run the app
    MainApp().run()