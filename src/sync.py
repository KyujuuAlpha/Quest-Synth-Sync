import requests
import zipfile
import os
import json

# URL constants
SR_BASE_URL = "https://synthriderz.com"
SR_API_PLAYLIST_DL_URL = "https://synthriderz.com/api/playlists/[ID]/download?v=2"
SR_API_PLAYLIST_URL = "https://synthriderz.com/api/playlists/[ID]?cache=0&join[]=items&join[]=items.beatmap&join[]=items.beatmap.files%7C%7Chash,download_url&join[]=items.beatmap.files.file%7C%7Cfilename"
# json.name (+ ".playlist" for playlist download name)
# json.download_url  (playlist download link)
# json.items[i].beatmap.files[0].download_url   (download link)
# json.items[i].beatmap.files[0].file.filename  (download name)

# Folder constants
CUSTOM_LEVEL_FOLDER = "/sdcard/Android/data/com.Kluge.SynthRiders/files/CustomSongs/"
CUSTOM_PLAYLIST_FOLDER = "/sdcard/Android/data/com.Kluge.SynthRiders/files/Playlist/"

# App config constants
APP_FOLDER = "/sdcard/QuestSynthSync/"
SAVED_PLAYLISTS = "saved_playlists.txt"

# retrieve data for a SynthRiderz playlist
def get_sr_songs(playlist_id):
    # build and send the SynthRiderz GET request
    sr_request = requests.get(SR_API_PLAYLIST_URL.replace("[ID]", playlist_id))

    # quick status code check
    if sr_request.status_code != requests.codes.ok:
        return None

    # extract the json
    sr_json = sr_request.json()

    # return the data
    return sr_json["name"], sr_json["items"]

# verify if the custom levels/playlists paths exists or not
def safe_path_check():
    # levels
    if os.path.exists(CUSTOM_LEVEL_FOLDER) == False:
        # create folder(s) if it does not exist
        os.makedirs(CUSTOM_LEVEL_FOLDER)
    
    # playlists
    if os.path.exists(CUSTOM_PLAYLIST_FOLDER) == False:
        # create folder(s) if it does not exist
        os.makedirs(CUSTOM_PLAYLIST_FOLDER)

# download a single song from SynthRiderz, returns true if it downloads
def download_song(song):
    # construct the download url and download location
    song_file = song["beatmap"]["files"][0]
    song_url = SR_BASE_URL + song_file["download_url"]
    download_location = CUSTOM_LEVEL_FOLDER + song_file["file"]["filename"]

    # basic check if it already exists or not
    if os.path.exists(download_location) == False:
        # download the file (streaming)
        with requests.get(song_url, stream=True) as response:
            # write the file (in chunks)
            with open(download_location, "wb") as file:
                for data_chunk in response.iter_content(chunk_size=1024):
                    if data_chunk:
                        file.write(data_chunk)
    else:
        return False

# create a playlist
def create_playlist(playlist_id, playlist_name):
    # construct the file location and data
    playlist_url = SR_API_PLAYLIST_DL_URL.replace("[ID]", playlist_id)
    playlist_location = CUSTOM_PLAYLIST_FOLDER + playlist_name + ".playlist"
    
    # basic check if it already exists or not
    if os.path.exists(playlist_location) == False:
        # download the file (streaming)
        with requests.get(playlist_url, stream=True) as response:
            # write the file (in chunks)
            with open(playlist_location, "wb") as file:
                for data_chunk in response.iter_content(chunk_size=1024):
                    if data_chunk:
                        file.write(data_chunk)
    else:
        return False

# safely check the existence of the app folder
def safe_app_path_check():
    if os.path.exists(APP_FOLDER) == False:
        # create folder(s) if it does not exist
        os.makedirs(APP_FOLDER)

# save the playlists input to a text file
def save_playlists(playlists):
    safe_app_path_check()

    # write to the file location
    with open(APP_FOLDER + SAVED_PLAYLISTS, "w") as playlist_file:
        playlist_file.write(playlists)

# load the user text file
def load_playlists():
    safe_app_path_check()

    playlist_file_location = APP_FOLDER + SAVED_PLAYLISTS
    playlist_text = ""

    # attempt to read from the file location if it exists
    if os.path.exists(playlist_file_location) == True:
        with open(playlist_file_location, "r") as playlist_file:
            playlist_text = playlist_file.readline()

    # return result
    return playlist_text