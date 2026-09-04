"""import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- Authentifizierung ---
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="7e75b19185924f00a4be022e1c4f7ccf",
    client_secret="804162953fd247c29f77bceaa19f4c6f"
))

# --- Beispiel: "Shape of You" von Ed Sheeran ---
track_id = "7qiZfU4dY1lWllzX7mPBI3"

# Audio Features abrufen
features = sp.audio_features([track_id])[0]

if features:
    print(f"Track ID: {track_id}")
    print(f"Tempo (BPM): {features['tempo']}")
    print(f"Danceability: {features['danceability']}")
    print(f"Energy: {features['energy']}")
else:
    print("Keine Features gefunden.")"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "7e75b19185924f00a4be022e1c4f7ccf"
CLIENT_SECRET = "804162953fd247c29f77bceaa19f4c6f"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

track_id = "7qiZfU4dY1lWllzX7mPBI3"  # Shape of You
features = sp.audio_features([track_id])[0]

if features:
    print("Tempo:", features["tempo"])
else:
    print("Keine Features gefunden.")
