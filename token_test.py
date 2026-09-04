#!/usr/bin/env python3
"""
debug_spotify.py
Einfaches Debug-Skript: holt ein Client-Credentials-Token und ruft die audio-features
für einen Track ab. Zeigt HTTP-Status und JSON-Antworten an.
Usage: python debug_spotify.py
Trag CLIENT_ID und CLIENT_SECRET in die Variablen unten ein.
"""

import sys, json
import requests

CLIENT_ID = "7e75b19185924f00a4be022e1c4f7ccf"
CLIENT_SECRET = "804162953fd247c29f77bceaa19f4c6f"
TRACK_ID = "7qiZfU4dY1lWllzX7mPBI3"  # Shape of You

def get_token():
    url = "https://accounts.spotify.com/api/token"
    try:
        r = requests.post(
            url,
            data={"grant_type": "client_credentials"},
            auth=(CLIENT_ID, CLIENT_SECRET),
            timeout=10
        )
    except Exception as e:
        print("Fehler beim Token-Request:", e)
        sys.exit(1)

    print("\n=== Token-Request ===")
    print("HTTP Status:", r.status_code)
    print("Response headers:", dict(r.headers))
    try:
        j = r.json()
        print("JSON Antwort (token endpoint):\n", json.dumps(j, indent=2))
    except Exception:
        print("Kein JSON, Body:\n", r.text)
        j = {}

    return r.status_code, j

def get_audio_features(access_token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("Fehler bei audio-features-Request:", e)
        sys.exit(1)

    print("\n=== Audio-Features-Request ===")
    print("URL:", url)
    print("HTTP Status:", r.status_code)
    try:
        print("JSON Antwort (audio-features):\n", json.dumps(r.json(), indent=2))
    except Exception:
        print("Body:\n", r.text)
    return r.status_code

def main():
    if CLIENT_ID.startswith("DEINE_") or CLIENT_SECRET.startswith("DEIN_"):
        print("Bitte CLIENT_ID und CLIENT_SECRET in das Skript eintragen und erneut ausführen.")
        sys.exit(1)

    status, token_json = get_token()

    if status != 200 or "access_token" not in token_json:
        print("\nFehler: Kein gültiger access_token erhalten. Bitte Ausgabe oben prüfen.")
        sys.exit(1)

    access_token = token_json["access_token"]
    print("\nAccess token (Anfang):", access_token[:30], "... Länge:", len(access_token))

    get_audio_features(access_token, TRACK_ID)

if __name__ == "__main__":
    main()
