import pickle
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def preprocess(dataset_path):
    data = pd.read_csv(dataset_path)
    data = data.dropna()
    data = data.drop_duplicates()
    data = data.reset_index(drop=True)

    return data

def train_model(file_name):
    dataset_path = f"/home/datasets/{file_name}"
    rules_path = "models/rules.pkl"
    songs_artists_path = "models/songs_artists.pkl"

    data = preprocess(dataset_path)
    songs_artists = dict(zip(data['track_name'], data['artist_name']))
    
    artist_most_freq_pid = data.groupby('artist_name')['pid'].apply(lambda x: x.value_counts().idxmax())
    df_onehot = data.groupby(['pid','artist_name'])['artist_name'].count().unstack().fillna(0)

    def encode_units(x):
        if x <= 0:
            return False
        if x >= 1:
            return True

    df_onehot = df_onehot.applymap(encode_units)
    frequent_itemsets = apriori(df_onehot, min_support=0.1, use_colnames=True, verbose=1)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.1)

    # Replace artist names in consequents with most frequent pid
    rules['consequents'] = rules['consequents'].apply(lambda x: set(artist_most_freq_pid[i] for i in x))

    rules.to_pickle(rules_path)
    with open(songs_artists_path, "wb") as f:
        pickle.dump(songs_artists, f)

if __name__ == "__main__":
    train_model("2023_spotify_ds1.csv")