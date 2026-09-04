# SpotifySongBPM

A small Python tool for exporting BPM and selected audio features from a Spotify playlist to a CSV file.

## Features

- Reads tracks from a Spotify playlist
- Exports the following audio features:
  - BPM (`tempo`)
  - Danceability
  - Energy
  - Valence
- Keeps track name and artist information
- Processes audio features in batches
- Supports a configurable output filename

## Requirements

- Python 3.9 or newer
- A Spotify Developer application
- A Spotify playlist that your account can access

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Spotify setup

Create an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and obtain its Client ID and Client Secret.

Add the following Redirect URI to your Spotify application:

```text
http://127.0.0.1:8000/callback
```

Set the credentials as environment variables. On Linux/macOS:

```bash
export SPOTIPY_CLIENT_ID="your-client-id"
export SPOTIPY_CLIENT_SECRET="your-client-secret"
```

Do not put your Client Secret directly into the source code or commit it to Git.

## Usage

Pass the Spotify playlist URL or URI as the first argument:

```bash
python main.py "https://open.spotify.com/playlist/your-playlist-id"
```

By default, the result is written to `playlist_bpm.csv`.

You can specify a different output file with `-o`:

```bash
python main.py "https://open.spotify.com/playlist/your-playlist-id" -o my_playlist.csv
```

## Output

The generated CSV contains these columns:

| Column | Description |
| --- | --- |
| `name` | Track name |
| `artist` | Artist or artists |
| `tempo` | Track tempo in BPM |
| `danceability` | Spotify's danceability value |
| `energy` | Spotify's energy value |
| `valence` | Spotify's musical positiveness value |

The generated CSV is ignored by Git via `.gitignore`.

## Project structure

```text
SpotifySongBPM/
├── main.py            # Main application
├── requirements.txt   # Python dependencies
├── .gitignore         # Ignored local/generated files
└── README.md          # Documentation
```

## Notes

The project originally contained several experimental scripts for authentication, HTTP requests, and testing. These have been removed in favor of a single main script with the playlist-processing functionality.

If you previously used a Spotify Client Secret that was committed to this repository, **rotate/revoke that secret in the Spotify Developer Dashboard**. Removing it from the current files does not remove it from Git history.
