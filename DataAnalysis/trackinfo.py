import spotipy
import pandas as pd
import numpy as np

from spotipy.oauth2 import SpotifyClientCredentials
cid = "NotMeantForYourEyes"
secret = "AlsoNotMeantForYourEyes;)"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

rock_count, pop_count, hip_hop_count, r_and_b_count = 0, 0, 0, 0

def searchBPM(track_uri):
    bpm = sp.audio_features(track_uri)[0].get('tempo')
    danceability = sp.audio_features(track_uri)[0].get('danceability')
    
    print(danceability)

def searchGenre(artist_name):
    global rock_count, pop_count, hip_hop_count, r_and_b_count, count
    
    result = sp.search(artist_name)

    if len(result['tracks']['items']) == 0:
        return
    else:
        track = result['tracks']['items'][0]
    
    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])

    for genre in artist["genres"]:
        if "rock" in genre:
            rock_count += 1
            break

    for genre in artist["genres"]:
        if "hip hop" in genre:
            hip_hop_count += 1
            break

    for genre in artist["genres"]:
        if "r&b" in genre:
            r_and_b_count += 1
            break

    for genre in artist["genres"]:
        if "pop" in genre:
            pop_count += 1
            break



#print(sp.audio_features("spotify:track:3hB5DgAiMAQ4DzYbsMq1IT"))

df = pd.read_csv("test.csv")
df = df[['track_uri', 'artist_name', 'track_name', 'album_name']]

print(df.head())
df = df.apply(lambda row: searchGenre(row['artist_name']), axis = 1)
df = df.apply(lambda row: searchBPM(row['track_uri']), axis = 1)
    
print("Rockcount: {0}, Popcount: {1}, Hiphop: {2}, R&B: {3}".format(rock_count, pop_count, hip_hop_count, r_and_b_count))
