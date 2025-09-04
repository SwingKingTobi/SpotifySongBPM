#!/bin/bash

# --- Konfiguration ---
CLIENT_ID="7e75b19185924f00a4be022e1c4f7ccf"
CLIENT_SECRET="804162953fd247c29f77bceaa19f4c6f"
REDIRECT_URI="http://127.0.0.1:8888/callback"
TRACK_ID="7qiZfU4dY1lWllzX7mPBI3"  # Shape of You

# --- Schritt 1: Authorization URL generieren ---
AUTH_URL="https://accounts.spotify.com/authorize?client_id=$CLIENT_ID&response_type=code&redirect_uri=$REDIRECT_URI&scope=user-read-private"
echo "Öffne diese URL im Browser, logge dich ein und kopiere den 'code' Parameter aus der Redirect-URL:"
echo $AUTH_URL
read -p "Gib hier den Code ein: " AUTH_CODE

# --- Schritt 2: Access Token abrufen ---
TOKEN_RESPONSE=$(curl -s -X POST "https://accounts.spotify.com/api/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=$AUTH_CODE&redirect_uri=$REDIRECT_URI&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET")

ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

# --- Schritt 3: Audio-Features abrufen ---
curl -s -X GET "https://api.spotify.com/v1/audio-features/$TRACK_ID" \
     -H "Authorization: Bearer $ACCESS_TOKEN" | jq
