from concurrent.futures import process
from turtle import position
import pandas as pd

from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from tqdm import tqdm
from mlxtend.preprocessing.transactionencoder import TransactionEncoder

#hier den FilePath zu der gewümschten file eintragen
filepath = "./testfiles/200.000 Schritte/test4.csv"


df = pd.read_csv(filepath)
df = df[['playlist_id', 'track_uri']]


def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

def itemQuanity(track_uri):

    return [1 for _ in range(len(track_uri))]


def createBasketv2():
    """ Creates basket as df from given Dataframe. is second approach. Much faster """
    basket = []
    playlistnb = df['playlist_id'][0]
    tracks = []
    print("--- Creating DF for Apriori ---")
    for index, row in tqdm(df.iterrows()):
        if playlistnb == row['playlist_id']:
            tracks.append(row['track_uri'])
        if playlistnb != row['playlist_id']:
            #if (row['playlist_id']) - int(playlistnb) > 1:
            #    print(playlistnb, " - ", row['playlist_id'])
            basket.append(tracks)
            tracks = []
            playlistnb = row['playlist_id']
            tracks.append(row['track_uri'])
    basket.append(tracks)

    #http://rasbt.github.io/mlxtend/user_guide/preprocessing/TransactionEncoder/
    te = TransactionEncoder()
    te_data = te.fit(basket).transform(basket)
    dfbasket = pd.DataFrame(te_data, columns=te.columns_)
    print(dfbasket.head())
    return dfbasket

def createbasketv1():
    """ Creates basket as df from given Dataframe. is first apprach. DON'T USE IT"""
    df2 = df.assign(test=itemQuanity(df['track_uri']))
    #inspired from https://practicaldatascience.co.uk/data-science/how-to-use-the-apriori-algorithm-for-market-basket-analysis
    baskets = df2.groupby(['playlist_id', 'track_uri'])['test'].sum().unstack().reset_index().fillna(0).set_index('playlist_id')
    baskets = baskets.applymap(encode_units)
    return baskets

#apriori alogrithm
def apriori():
    """Creates rules form Basket"""

    basket = createBasketv2()
    #creates Itemsets
    print("--- Create itemsets ---")
    itemsets = fpgrowth(basket, use_colnames=True, verbose=0, min_support=0.001, max_len=3)

    #print(itemsets)

    #create Assoziation rules

    print("--- Creating Rules ---")
    rules = association_rules(itemsets, metric="lift", min_threshold=1)
    rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])

    higherCnf = rules[(rules['confidence'] >= 0.6)]
    print(higherCnf)

    return rules


def rulesToCsv(rules):
    """Writes ruls in a csv file """

    rulefile = open("rules.csv", "a")
    print("Write rules in file")
    for index, rule in tqdm(rules.iterrows()):
        line = "".join(f'{antecedent} ' for antecedent in rule['antecedents'])
        line += "- "
        for consequent in rule['consequents']:
            line += f'{consequent} '
        line += "\n"
        rulefile.write(line)


def main():
    rules = apriori()
    rulesToCsv(rules)

if __name__ == "__main__":
    main()

