from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
rules = pd.read_pickle('./../models/rules.pkl')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    songs = request.json['songs']
    recommendations = []
    
    for song in songs:
        matched_rules = rules[rules['antecedents'].apply(lambda x: song in x)]
        if not matched_rules.empty:
            recommendations.extend(matched_rules['consequents'].iloc[0])
    
    recommendations = list(set(recommendations))
    
    return jsonify({
        "playlist_ids": recommendations,
        "version": "1.0",
        "model_date": "2023-10-25"
    })

if __name__ == '__main__':
    app.run(port=30500)
