import pickle
import sys
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def preprocess(file_name):
    data = pd.read_csv(f"datasets/{file_name}")
    data = data.dropna()
    data = data.drop_duplicates()
    data = data.reset_index(drop=True)

    return data

def train_model(file_name):
    data = preprocess(file_name)
    songs_artists = dict(zip(data['track_name'], data['artist_name']))
    
    artist_most_freq_pid = data.groupby('artist_name')['pid'].apply(lambda x: x.value_counts().idxmax())
    df_onehot = data.groupby(['pid','artist_name'])['artist_name'].count().unstack().fillna(0)

    def encode_units(x):
        if x <= 0:
            return False
        if x >= 1:
            return True

    df_onehot = df_onehot.applymap(encode_units)
    frequent_itemsets = apriori(df_onehot, min_support=0.008, use_colnames=True, verbose=1)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.001)

    # Replace artist names in consequents with most frequent pid
    rules['consequents'] = rules['consequents'].apply(lambda x: set(artist_most_freq_pid[i] for i in x))

    if debug_mode:
        # print("DEBUG => TRANSACTIONS:\n\n", transactions)
        # print()
        print("DEBUG => FREQUENT ITEMSETS:\n\n", frequent_itemsets)
        print()
        print("DEBUG => POSSIBLE RULES:\n\n", rules)

    else:
        rules.to_pickle(f"../models/rules.pkl")
        with open("../models/songs_artists.pkl", "wb") as f:
            pickle.dump(songs_artists, f)


debug_mode = False
if __name__ == "__main__":
    if "--debug" in sys.argv:
        debug_mode = True

    train_model("playlist-sample-ds1.csv")