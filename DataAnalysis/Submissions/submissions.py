from os import system
import pandas as pd
from tqdm import tqdm
import multiprocessing
import sys


df = pd.read_json("C:\\Users\\Is4ki\\Desktop\\spotify_million_playlist_dataset_challenge\\challenge_set.json")
df = df[['playlists']]
dictChallengeSet = {}
for index, val in df.iterrows():
    for playlist in val:
        if playlist['pid'] in dictChallengeSet:
            dictChallengeSet[playlist['pid']].append(track['track_uri'])
        else:
            dictChallengeSet[playlist['pid']] = []
        for track in playlist['tracks']:
            if playlist['pid'] in dictChallengeSet:
                dictChallengeSet[playlist['pid']].append(track['track_uri'])
            else:
                dictChallengeSet[playlist['pid']] = [track['track_uri']]

f = open("rules.csv", "r")

print("Create file")
submissions = open("submissions.csv", "a")
print(len(dictChallengeSet))
for key, val in tqdm(dictChallengeSet.items()):
    ergline = str(key)
    lessThan50 = 0

    for rule in open("rules.csv", "r"):
        if lessThan50 >= 500:
            break
        acceptRule = True
        rule = rule.split("-")

        #print("antecedent ---- ",rule[0].strip().split(" "))
        #print("consequent ---- ",rule[1].strip().split(" "))
        for antecedent in rule[0].strip().split(" "):
            if antecedent not in val:
                acceptRule = False
        if acceptRule is True:
            for consequent in rule[1].strip().split(" "):
                if consequent not in val and consequent not in ergline:
                    ergline += f", {consequent}"
                    lessThan50 += 1
    
    if lessThan50 < 500:
        for key, value in dictChallengeSet.items():
            if lessThan50 == 500:
                break
            for track in value:
                if lessThan50 == 500:
                    break
                if track not in ergline and track not in val:
                    ergline += f", {track}"
                    lessThan50 += 1
    
    ergline += '\n\n'
    submissions.write(ergline)

