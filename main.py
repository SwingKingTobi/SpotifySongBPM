import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "7e75b19185924f00a4be022e1c4f7ccf"
CLIENT_SECRET = "804162953fd247c29f77bceaa19f4c6f"
REDIRECT_URI = "http://127.0.0.1:9090/callback"

scope = "user-read-private"  # reicht, du brauchst keine großen Scopes für Audio Features

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
    open_browser=True
))

# Test: Audio-Features eines Songs
track_id = "7qiZfU4dY1lWllzX7mPBI3"  # Shape of You
features = sp.audio_features([track_id])[0]

print("Tempo:", features["tempo"])
print("Alle Features:", features)
