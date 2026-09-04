import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- Konfiguration ---
CLIENT_ID="7e75b19185924f00a4be022e1c4f7ccf"
CLIENT_SECRET="804162953fd247c29f77bceaa19f4c6f"
REDIRECT_URI="http://127.0.0.1:8888/callback"
scope="user-library-read"
TRACK_ID = "7qiZfU4dY1lWllzX7mPBI3"  # Shape of You

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="DEINE_CLIENT_ID",
    client_secret="DEIN_CLIENT_SECRET",
    redirect_uri="http://127.0.0.1:8888/callback",

))

features = sp.audio_features([TRACK_ID])[0]
print(features)
