from flask import Flask, request, jsonify
import pandas as pd
import sys
import pickle
import random
from datetime import datetime

app = Flask(__name__)

def recommend(songs):
    rules_path = "models/rules.pkl"
    songs_artists_path = "models/songs_artists.pkl"

    song_artist_map = dict()
    with open(songs_artists_path, "rb") as f:
        song_artist_map = pickle.load(f)

    recommendations = []

    rules = pd.read_pickle(rules_path)
    for song in songs:
        artist = song_artist_map.get(song, None)

        if artist is not None:
            matched_rules = rules[rules['antecedents'].apply(lambda x: artist in x)]

            if not matched_rules.empty:
                recommendations.extend(matched_rules['consequents'].iloc[0])
    
    recommendations = list(set(recommendations))

    if len(recommendations) == 0: # The model can not recommend anything, so apply a random recommendation
        random.seed(len([c for song in songs for c in song]))
        index = random.randint(0, len(rules) - 1)
        random_recommendation = rules["consequents"].iloc[index]
        recommendations.extend(random_recommendation)
    
    return [int(item) for item in recommendations]

@app.route('/api/recommend', methods=['POST'])
def recommendApi():
    songs = request.json['songs']
    
    recommendations = recommend(songs)

    current_datetime = datetime.now()
    model_date = current_datetime.strftime("%Y-%m-%d")
    version = current_datetime.strftime("%Y.%m.%d.%H.%M.%S")

    return jsonify({
        "playlist_ids": recommendations,
        "version": version,
        "model_date": model_date
    })

if __name__ == '__main__':
    app.run(debug=True, port=32171, host="0.0.0.0")

