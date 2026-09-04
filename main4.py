import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- Konfiguration ---
CLIENT_ID = "7e75b19185924f00a4be022e1c4f7ccf"
CLIENT_SECRET = "804162953fd247c29f77bceaa19f4c6f"
REDIRECT_URI = "http://127.0.0.1:8000/callback"

# Track-ID: Beispiel "Shape of You"
TRACK_ID = "7qiZfU4dY1lWllzX7mPBI3"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-private"   # reicht schon
))

features = sp.audio_features(TRACK_ID)[0]
print(features["tempo"])

""""# --- Authentifizierung ---
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-private",   # minimale Berechtigung
    open_browser=True            # öffnet automatisch den Browser
))

# Einzelner Track
features = sp.audio_features(TRACK_ID)[0]
print(features)


# --- Audio Features abrufen ---
features = sp.audio_features([TRACK_ID])[0]

# --- Ergebnis anzeigen ---
if features:
    print("🎵 Song-ID:", TRACK_ID)
    print("Tempo (BPM):", features["tempo"])
    print("Alle Features:")
    for key, value in features.items():
        print(f"  {key}: {value}")
else:
    print("⚠️ Keine Features gefunden.")"""
