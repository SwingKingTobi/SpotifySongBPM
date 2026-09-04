import requests
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "7e75b19185924f00a4be022e1c4f7ccf"
CLIENT_SECRET = "804162953fd247c29f77bceaa19f4c6f"
REDIRECT_URI = "http://127.0.0.1:9090/callback"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=""  # kein Scope notwendig für Audio Features
)

# Hol das Token
token_info = sp_oauth.get_access_token(as_dict=True)
access_token = token_info["access_token"]

print("Access Token:", access_token[:40], "...")

# Test-Request mit requests statt Spotipy
track_id = "7qiZfU4dY1lWllzX7mPBI3"
url = f"https://api.spotify.com/v1/audio-features/{track_id}"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(url, headers=headers)
print("HTTP Status:", response.status_code)
print("Antwort:", response.text)
