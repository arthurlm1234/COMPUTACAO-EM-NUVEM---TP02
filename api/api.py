from flask import Flask, request, jsonify
import pandas as pd
import sys
import pickle
import random

app = Flask(__name__)
rules = pd.read_pickle('/app/models/rules.pkl')

def recommend(songs):
    # Load song-artist mapping
    song_artist_map = dict()
    with open("/app/models/songs_artists.pkl", "rb") as f:
        song_artist_map = pickle.load(f)

    recommendations = []
    
    if debug_mode:
        print("DEBUG => RULES:\n\n", rules)
        print()

    for song in songs:
        # Get the artist of the song
        artist = song_artist_map.get(song, None)
        if artist is not None:
            # Find rules where this artist is in the antecedents
            matched_rules = rules[rules['antecedents'].apply(lambda x: artist in x)]
            if not matched_rules.empty:
                recommendations.extend(matched_rules['consequents'].iloc[0])
    
    recommendations = list(set(recommendations))
    if len(recommendations) == 0: # The model can not recommend anything, so apply a random recommendation
        random.seed(len([c for song in songs for c in song]))
        index = random.randint(0, len(rules) - 1)
        random_recommendation = rules["consequents"].iloc[index]
        recommendations.extend(random_recommendation)
    
    recommendations = [int(item) for item in recommendations]

    return recommendations

@app.route('/api/recommend', methods=['POST'])
def recommendApi():
    songs = request.json['songs']
    
    recommendations = recommend(songs)
    return jsonify({
        "playlist_ids": recommendations,
        "version": "1.0",
        "model_date": "2023-10-25"
    })

def debugRecommendation():
    # songs = ["I Was Married", "Hop A Plane", "Otra Vez (feat. J Balvin)", "Pierdo la Cabeza - Official Remix", "Ay Mi Dios"]
    songs = ["Back In Your Head"]
    # songs = ["HUMBLE."]
    # songs = ["Force of Nature"]


    recommendations = recommend(songs)

    print("DEBUG => RECOMMENDATIONS:\n", recommendations)
    print()

debug_mode = False
if __name__ == '__main__':
    songs_artists = pd.read_pickle('/app/models/songs_artists.pkl')
    
    if "--debug" in sys.argv:
        debug_mode = True
        debugRecommendation()

    else:
        app.run(port=32215)
