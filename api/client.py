import requests
import json
import sys

API_URL = "http://localhost:30500/api/recommend"

def get_recommendations(songs):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'songs': songs
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <song1> <song2> ...")
        sys.exit(1)

    songs = sys.argv[1:]
    recommendations = get_recommendations(songs)

    if recommendations:
        print("Recommended Playlist IDs:", recommendations['playlist_ids'])