#!/usr/bin/env python3
"""Export BPM and selected audio features for a Spotify playlist."""

import argparse
import os
from pathlib import Path

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth


REDIRECT_URI = "http://127.0.0.1:8000/callback"
SCOPE = "playlist-read-private"


def create_spotify_client() -> spotipy.Spotify:
    """Create an authenticated Spotipy client from environment variables."""
    client_id = os.environ.get("SPOTIPY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET before running the script."
        )

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
        )
    )


def get_playlist_tracks(sp: spotipy.Spotify, playlist_uri: str) -> list[dict[str, str]]:
    """Return the Spotify tracks in a playlist."""
    tracks = []
    results = sp.playlist_items(playlist_uri)

    while results:
        for item in results["items"]:
            track = item.get("track")
            if track and track.get("id"):
                tracks.append(
                    {
                        "id": track["id"],
                        "name": track["name"],
                        "artist": ", ".join(
                            artist["name"] for artist in track["artists"]
                        ),
                    }
                )
        results = sp.next(results) if results["next"] else None

    return tracks


def get_audio_features(sp: spotipy.Spotify, tracks: list[dict[str, str]]) -> list[dict]:
    """Fetch audio features in batches and combine them with track metadata."""
    rows = []

    for start in range(0, len(tracks), 100):
        batch = tracks[start : start + 100]
        features = sp.audio_features([track["id"] for track in batch])

        for track, feature in zip(batch, features):
            if feature is None:
                continue
            rows.append(
                {
                    "name": track["name"],
                    "artist": track["artist"],
                    "tempo": feature["tempo"],
                    "danceability": feature["danceability"],
                    "energy": feature["energy"],
                    "valence": feature["valence"],
                }
            )

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("playlist", help="Spotify playlist URL or URI")
    parser.add_argument(
        "-o",
        "--output",
        default="playlist_bpm.csv",
        help="Output CSV file (default: playlist_bpm.csv)",
    )
    args = parser.parse_args()

    sp = create_spotify_client()
    tracks = get_playlist_tracks(sp, args.playlist)
    print(f"Found {len(tracks)} tracks.")

    rows = get_audio_features(sp, tracks)
    pd.DataFrame(rows).to_csv(Path(args.output), index=False)
    print(f"Saved BPM data for {len(rows)} tracks to {args.output}")


if __name__ == "__main__":
    main()
