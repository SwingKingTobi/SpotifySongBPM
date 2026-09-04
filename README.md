# SpotifySongBPM

A small Python project for retrieving Spotify playlist information and exporting BPM and selected audio features to CSV.

> **Current status:** Spotify's 2026 Web API changes mean that the `audio-features` endpoint may return `403 Forbidden` for Development Mode applications. As a result, the BPM/audio-feature export is currently **not reliably available through the Spotify Web API** for this project.

## Features

The project is designed to:

- Read tracks from a Spotify playlist
- Retrieve track metadata
- Retrieve Spotify audio features such as:
  - BPM (`tempo`)
  - Danceability
  - Energy
  - Valence
- Export the results to CSV
- Process audio features in batches

The current implementation successfully retrieves playlist tracks, but the audio-feature request can fail with HTTP 403 under Spotify's current API restrictions.

## Requirements

- Python 3.9 or newer
- A Spotify Developer application
- A Spotify Premium account for Development Mode apps
- A Spotify playlist that your account can access

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Spotify API changes in 2026

Spotify changed the Web API rules for Development Mode applications in 2026. Existing Development Mode apps were migrated to the new restrictions on **March 9, 2026**.

Among other restrictions, Development Mode apps now require the app owner to have an active Spotify Premium subscription and are limited to up to five authenticated users. Users other than the app owner must be added to the app's allowlist.

Spotify's documentation also notes that some API functionality and endpoints have been removed or changed. Extended Quota Mode applications are not affected by the February 2026 migration changes.

For details, see Spotify's official documentation:

- [February 2026 Web API Migration Guide](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide)
- [Web API Changelog – February 2026](https://developer.spotify.com/documentation/web-api/references/changes/february-2026)
- [Quota modes](https://developer.spotify.com/documentation/web-api/concepts/quota-modes)

### The `audio-features` problem

`main.py` uses Spotipy's `audio_features()` method to request Spotify's audio-feature data. For example, a playlist can be read successfully:

```text
Found 46 tracks.
```

but the subsequent request to:

```text
GET /v1/audio-features/?ids=...
```

may return:

```text
403 Forbidden
```

This means that successful OAuth authentication and playlist access do **not** necessarily imply that audio-feature access is available.

This is an API access issue rather than a Python authentication or redirect-URI issue.

## Spotify setup

Create an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and obtain its Client ID and Client Secret.

The application should use the following Redirect URI:

```text
http://127.0.0.1:9090/callback
```

The Redirect URI configured in the Spotify Developer Dashboard must exactly match the URI used by the application.

Set the credentials as environment variables. On Linux/macOS:

```bash
export SPOTIPY_CLIENT_ID="your-client-id"
export SPOTIPY_CLIENT_SECRET="your-client-secret"
```

Do **not** put the Client Secret directly into the source code or commit it to Git.

### Authentication cache

Spotipy stores authentication information in a local cache. If authentication behaves unexpectedly after changing the application configuration, remove the local cache and authenticate again:

```bash
rm -rf .cache
```

The `.cache/` directory is ignored by Git.

## Usage

Pass the Spotify playlist URL or URI as the first argument:

```bash
python main.py "https://open.spotify.com/playlist/your-playlist-id"
```

By default, the result is written to:

```text
playlist_bpm.csv
```

You can specify a different output file:

```bash
python main.py "https://open.spotify.com/playlist/your-playlist-id" -o my_playlist.csv
```

## Output

When Spotify provides the audio features, the generated CSV contains:

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

## Security

The original repository contained Spotify credentials directly in several experimental scripts. Those credentials have been removed from the current project files and authentication now uses environment variables.

However, removing a secret from the current files does **not** remove it from Git history. If a real Spotify Client Secret was previously committed, it should be **rotated/revoked in the Spotify Developer Dashboard**.

## Possible future directions

If Spotify continues to restrict access to audio features for Development Mode applications, the project could be extended in one of these directions:

1. Investigate whether the Spotify application can use Extended Quota Mode.
2. Keep Spotify integration for playlist and track metadata while obtaining BPM data from another permitted source.
3. Add local audio analysis, for example with `librosa`, for audio files that the user is legally able to analyze.

The project should not download or rip Spotify audio in order to work around Spotify's API restrictions.
