import pandas as pd

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules



def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

def itemQuanity(track_uri):
    a = []
    for i in range(len(track_uri)):
        a.append(1)
    return a
#todos:

#crate data with items
df = pd.read_csv("test.csv")
df = df[['playlist_id', 'track_uri']]
df2 = df.assign(test=itemQuanity(df['track_uri']))

#inspired from https://practicaldatascience.co.uk/data-science/how-to-use-the-apriori-algorithm-for-market-basket-analysis
baskets = df2.groupby(['playlist_id', 'track_uri'])['test'].sum().unstack().reset_index().fillna(0).set_index('playlist_id')
baskets = baskets.applymap(encode_units)
#print(baskets.head())

playlistdict = dict()
for index, row in df.iterrows():
    if row['playlist_id'] not in playlistdict:
        playlistdict[row['playlist_id']] = [row['track_uri']]
    else:
        playlistdict[row['playlist_id']].append(row['track_uri'])


#apriori alogrithm

itemsets = apriori(baskets, use_colnames=True, verbose=1, low_memory=False, min_support=0.01, max_len=3)

#print(itemsets)

#create Assoziation rules
rules = association_rules(itemsets, metric="lift", min_threshold=1)
rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
print(rules)

count = 0
for entry in rules['confidence']:
    if entry >= 0.75:
        count += 1

print("Number of Tracks with >= 0.75: {0}".format(count))
higherCnf = rules[(rules['confidence'] >= 0.50)]
print(higherCnf)

submissions = open("submissions.csv","w")
for key, val in playlistdict.items():
    ergline = str(key)
    lessThan50 = 0
    i = 0
    for index, rule in rules.iterrows():
        if lessThan50 >= 50:
            break

        acceptRule = True
        i += 1
        for antecedent in rule['antecedents']:
            if antecedent not in val:
                acceptRule = False
        if acceptRule is True:
            for consequent in rule['consequents']:

                if consequent not in val and consequent not in ergline:
                    ergline += f", {consequent}"
                    lessThan50 +=1
    ergline += "\n"
    submissions.write(ergline)



#print(higherCnf.confidence.to_string(index=False))
