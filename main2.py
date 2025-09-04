import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time

# ---- CONFIG ----
CLIENT_ID = "7e75b19185924f00a4be022e1c4f7ccf"
CLIENT_SECRET = "804162953fd247c29f77bceaa19f4c6f"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-read-private"
PLAYLIST_URI = "https://open.spotify.com/playlist/75eHKygH6xmfhgepgYMoW9"  # Beispiel

# ---- AUTH ----
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# ---- TRACKS ABRUFEN ----
def get_playlist_tracks(sp, playlist_uri):
    results = sp.playlist_items(playlist_uri)
    tracks = []
    while results:
        for item in results['items']:
            track = item['track']
            if track:
                tracks.append({
                    "id": track['id'],
                    "name": track['name'],
                    "artist": ", ".join([a['name'] for a in track['artists']])
                })
        # Pagination
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return tracks

tracks = get_playlist_tracks(sp, PLAYLIST_URI)

# ---- AUDIO-FEATURES ABRUFEN ----
features_list = []
for track in tracks:
    try:
        features = sp.audio_features(track['id'])[0]
        if features:
            features_list.append({
                "name": track['name'],
                "artist": track['artist'],
                "danceability": features['danceability'],
                "energy": features['energy'],
                "tempo": features['tempo'],
                "valence": features['valence']
            })
        else:
            print(f"Skipping {track['name']} by {track['artist']}: No features returned")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Skipping {track['name']} by {track['artist']}: {e}")
    time.sleep(0.1)  # kleine Pause, um Rate-Limit zu vermeiden

# ---- CSV SPEICHERN ----
df = pd.DataFrame(features_list)
df.to_csv("playlist_bpm.csv", index=False)
print(f"Saved BPM data for {len(features_list)} tracks to playlist_bpm.csv")
