# CONNECT TO SPOTIFY
# set credentials
CLIENT_ID = 'a8d1e08f38b047beb8214857a06874bf'
CLIENT_SECRET = '8c8fa811a339487c874697fb849e3f58'

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager = 
                          SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def get_audio_features(track_id):
    while True:
        try:
            return spotify.audio_features(track_id)
        except:
            pass

def get_track_data(track_id):
    while True:
        try:
            return spotify.track(track_id)
        except:
            pass