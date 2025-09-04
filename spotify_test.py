import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- Set your credentials here if not using environment variables ---
# os.environ["SPOTIPY_CLIENT_ID"] = "7e75b19185924f00a4be022e1c4f7ccf"
# os.environ["SPOTIPY_CLIENT_SECRET"] = "804162953fd247c29f77bceaa19f4c6f"

try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    # Test: fetch Spotify “categories” (public endpoint)
    categories = sp.categories(limit=1)
    print("Connection successful! Here's one category from Spotify:")
    print(categories["categories"]["items"][0]["name"])
except Exception as e:
    print("Connection failed:")
    print(e)
