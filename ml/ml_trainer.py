import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def train_model(file_name):
    data = pd.read_csv(f"datasets/{file_name}")
    transactions = data.groupby('pid')['track_name'].apply(list)

    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)

    df = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

    rules.to_pickle(f"../models/rules.pkl")


if __name__ == "__main__":
    train_model("playlist-sample-ds1.csv")