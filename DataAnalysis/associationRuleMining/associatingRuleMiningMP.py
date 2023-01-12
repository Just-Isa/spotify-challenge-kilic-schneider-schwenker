from concurrent.futures import process
from turtle import position
import pandas as pd

from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from tqdm import tqdm
from mlxtend.preprocessing.transactionencoder import TransactionEncoder
import multiprocessing



def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

def itemQuanity(track_uri):
    return [1 for _ in range(len(track_uri))]

def fillDf(durchlaufrange):
    global basket 
       
    if durchlaufrange == 1:
        von, bis = 1, 6
    elif durchlaufrange == 2:
        von, bis = 6, 12
    elif durchlaufrange == 3:
        von, bis = 12, 18
    elif durchlaufrange == 4:
        von, bis = 18, 24
    #crate data with items    
    for i in tqdm(range(von, bis)):
        
        testFilePath = "E:\\Data Science\\Spotify-Challenge-Kilic-Schneider-Schwenker\\DataAnalysis\\testfiles\\test"+str(i)+".csv"
        print(testFilePath)
        df = pd.read_csv(testFilePath)
        df = df[['playlist_id', 'track_uri']]
        #df2 = df.assign(test=itemQuanity(df['track_uri']))
        basket = []
        playlistnb = df['playlist_id'][0]
        tracks = []
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
    dfb = pd.DataFrame(te_data, columns=te.columns_)
    print(dfb)

    '''
    #inspired from https://practicaldatascience.co.uk/data-science/how-to-use-the-apriori-algorithm-for-market-basket-analysis
    baskets = df2.groupby(['playlist_id', 'track_uri'])['test'].sum().unstack().reset_index().fillna(0).set_index('playlist_id')
    baskets = baskets.applymap(encode_units)
    print(baskets)
    '''
    
    #apriori alogrithm

    itemsets = fpgrowth(dfb, use_colnames=True, verbose=0, min_support=0.001, max_len=3)

    #print(itemsets)

    #create Assoziation rules
    rules = association_rules(itemsets, metric="lift", min_threshold=1)
    rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
    print(rules)

    higherCnf = rules[(rules['confidence'] >= 0.6)]
    print(higherCnf)

    "track1 track2 - tracky"
    #higherCnf.to_csv('rules.csv',sep="\t", encoding='UTF-8')
    rulefile = open("rules.csv", "a")

    for index, rule in tqdm(higherCnf.iterrows()):
        line = ""
        for antecedent in rule['antecedents']:
            line += antecedent+" "
        line += "- "
        for consequent in rule['consequents']:
            line += consequent+" "
        line += "\n"
        rulefile.write(line)


if __name__ == '__main__':
    processes = []    
    for i in range (1, 5):
        t = multiprocessing.Process(target=fillDf, args=(i,))
        processes.append(t)
        t.start()
    for i in range(4):
        processes[i].join()    




