import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def recommend_playlists(liked_songs):
    rules = pd.read_pickle(f"../models/rules.pkl")

    # Filtra as regras que tem pelo menos um item que o usuário gosta
    filtered_rules = rules[rules['antecedents'].apply(lambda x: any(item for item in liked_songs if item in x))]
    recommended_songs = filtered_rules['consequents']

    return recommended_songs


liked_songs = ['HUMBLE.', 'Mask Off']
recommendations = recommend_playlists(liked_songs)
print(recommendations)