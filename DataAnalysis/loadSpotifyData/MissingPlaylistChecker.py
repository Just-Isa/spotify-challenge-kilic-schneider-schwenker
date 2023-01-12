import pandas as pd


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

playlistlist = []
for line in open("submissions.csv", "r"):
    newline = line.split(",")
    if newline[0] != '\n' and newline[0] != 'team_info':
        playlistlist.append(int(newline[0]))
        
    
for key in dictChallengeSet.keys():
    if int(key) not in playlistlist:
        print(key)