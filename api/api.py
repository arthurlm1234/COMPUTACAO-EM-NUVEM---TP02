from flask import Flask, request, jsonify
import pandas as pd
import sys
import pickle

app = Flask(__name__)
rules = pd.read_pickle('./../models/rules.pkl')

def recommend(songs):
    # Load song-artist mapping
    song_artist_map = dict()
    with open("./../models/songs_artists.pkl", "rb") as f:
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
        index = hash("".join(songs)) % len(rules)
        random_recommendation = rules["consequents"].iloc[index]
        recommendations.extend(random_recommendation)

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
    songs_artists = pd.read_pickle('./../models/songs_artists.pkl')
    
    if "--debug" in sys.argv:
        debug_mode = True
        debugRecommendation()

    else:
        app.run(port=30500)
