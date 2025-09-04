import os
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# ----------------------------
# 1. Authentication
# ----------------------------
# Make sure these environment variables are set:
# SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
# Example (Mac/Linux):
#export SPOTIPY_CLIENT_ID="7e75b19185924f00a4be022e1c4f7ccf"
#export SPOTIPY_CLIENT_SECRET="804162953fd247c29f77bceaa19f4c6f"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# ----------------------------
# 2. Playlist URI
# ----------------------------
# Replace with your playlist URI or URL
PLAYLIST_URI = "https://open.spotify.com/playlist/33OfuMTc0ouqa88abnE1tO"

# ----------------------------
# 3. Fetch all tracks from playlist
# ----------------------------
def get_playlist_tracks(sp, playlist_uri):
    results = sp.playlist_tracks(playlist_uri)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks

tracks = get_playlist_tracks(sp, PLAYLIST_URI)

# ----------------------------
# 4. Extract BPM and save to CSV
# ----------------------------
with open("playlist_bpm.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Artist", "Track", "BPM"])  # header row

    for item in tracks:
        track = item["track"]
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]

        try:
            features = sp.audio_features(track["id"])[0]
            if features:
                tempo = features["tempo"]
            else:
                tempo = None
        except spotipy.exceptions.SpotifyException as e:
            print(f"Skipping {track_name} by {artist_name}: {e}")
            tempo = None


print(f"Saved BPM data for {len(tracks)} tracks to playlist_bpm.csv")

