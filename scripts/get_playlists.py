import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# grab env vars
load_dotenv()

# client_id, client_secret, and redirect_uri are set via the Spotify developer dashboard
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = os.getenv("redirect_uri")

# initialize Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-library-read'))

my_spotify_playlists = dict()

# function to get all songs & their info from a playlist
def get_songs(playlist_id):
    songs = sp.playlist_tracks(playlist_id)
    
    return songs

# function to get all playlist info
def get_all_playlists():
    playlists = sp.current_user_playlists()
    
    while playlists:
        for playlist in playlists['items']:
            my_spotify_playlists[playlist['id']] = dict()
            my_spotify_playlists[playlist['id']]['name'] = playlist['name']
            my_spotify_playlists[playlist['id']]['collaborative'] = playlist['collaborative']
            my_spotify_playlists[playlist['id']]['description'] = playlist['description']
            my_spotify_playlists[playlist['id']]['songs'] = get_songs(playlist['id'])
        
        # check if there are more pages of results & go to the next page if so
        if playlists['next']:
                playlists = sp.next(playlists)
        else:
            playlists = None

    return my_spotify_playlists

playlist_ids = get_all_playlists()

    
with open ("../results/rebeccahendsey_playlists.json", "w") as outfile:    
    json.dump(playlist_ids, outfile)


