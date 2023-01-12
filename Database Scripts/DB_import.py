import pandas as pd
import json
import sys
import psycopg2 as ps
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
from time import sleep
from tqdm import tqdm
import multiprocessing

counter = 1
connectionex = {
    "host":"localhost",
    "port":"9001",
    "database":"pschn004_Spotify",
    "user":"pschn004",
    "password":"test",
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 5,
    "keepalives_count": 5,
}

try:
    cnx2 = ps.connect(**connectionex)
    c2 = cnx2.cursor()
except:
    print("didnt work fella")
    sys.exit(1)

def queries(durchlaufrange):  # sourcery no-metrics  Weird error, macht nichts aus 
    global c2, cnx2, counter
    files = ["..\Playlists\mpd.slice.591000-591999.json", "..\Playlists\mpd.slice.595000-595999.json","..\Playlists\mpd.slice.596000-596999.json",
             "..\Playlists\mpd.slice.597000-597999.json", "..\Playlists\mpd.slice.580000-580999.json","..\Playlists\mpd.slice.600000-600999.json",
             "..\Playlists\mpd.slice.601000-601999.json","..\Playlists\mpd.slice.605000-605999.json","..\Playlists\mpd.slice.606000-606999.json",
             "..\Playlists\mpd.slice.607000-607999.json","..\Playlists\mpd.slice.564000-564999.json","..\Playlists\mpd.slice.568000-568999.json",]
    
    track_set = set()
    
    if durchlaufrange == 1:
        von, bis = 0, 1  
    elif durchlaufrange == 2:
        von, bis = 1, 2  
    elif durchlaufrange == 3:
        von, bis = 2, 3
    elif durchlaufrange == 4:
        von, bis = 3, 4
    elif durchlaufrange == 5:
        von, bis = 4, 5 
    elif durchlaufrange == 6:
        von, bis = 5, 6
    elif durchlaufrange == 7:
        von, bis = 6, 7 
    elif durchlaufrange == 8:
        von, bis = 7, 8 
    elif durchlaufrange == 9:
        von, bis = 8, 9 
    elif durchlaufrange == 10:
        von, bis = 9, 10
    elif durchlaufrange == 11:
        von, bis = 10, 11 
    elif durchlaufrange == 12:
        von, bis = 11, 12
        
    albumquery = ""
    artistquery = ""
    
    for i in tqdm(range(von, bis)):
        data = json.load(open(files[i], encoding="utf-8"))
        df = pd.DataFrame(data["playlists"])
        track_pos_playlist_query = ""
        '''
        playlistquery = "".join(
            "INSERT INTO playlist(playlist_name, playlist_id, modified_at, num_tracks, num_albums, num_followers, collaborative) VALUES ('"
            + str(row["name"]).replace("'", '')
            + "','"
            + str(row["pid"])
            + "','"
            + str(row["modified_at"])
            + "','"
            + str(row["num_tracks"])
            + "','"
            + str(row["num_albums"])
            + "','"
            + str(row["num_followers"])
            + "','"
            + str(row["collaborative"])
            + "') ON CONFLICT(playlist_id) DO NOTHING;"
            for index, row in df.iterrows()
        )
        c2.execute(playlistquery)
        '''
        for index, rows in df.iterrows():
            # artists name
            for name in rows["tracks"]:
                    albumquery += "INSERT INTO album(album_uri, album_name) VALUES('"+str(name['album_uri'])+"','"+str(name['album_name']).replace("'", "")+"') ON CONFLICT(album_uri) DO NOTHING;"
                    artistquery += "INSERT INTO artist(artist_uri, artist_name) VALUES('" +str(name['artist_uri']) +"','" +str(name['artist_name']).replace("'", "") +"') ON CONFLICT(artist_uri) DO NOTHING;"

                    '''
                    track_dict = {}
                    if name['track_uri']:
                        track_dict['track_uri'] = str(name['track_uri'])
                        track_dict['track_name'] = str(name['track_name'])
                        track_dict['duration_ms'] = str(name['duration_ms'])
                        track_dict['artist_uri'] = str(name['artist_uri'])
                        track_dict['album_uri'] = str(name['album_uri'])
                        track_set.add(tuple(track_dict.items()))
                    '''
                    track_pos_playlist_query += "INSERT INTO track_pos_playlist(playlist_id, track_uri, track_pos)VALUES('"+ str(rows["pid"]) + "','"+ str(name['track_uri']) + "','"+ str(name["pos"]) + "') ON CONFLICT(playlist_id, track_uri) DO NOTHING;"
        c2.execute(track_pos_playlist_query)    
        cnx2.commit()
    '''
    trackquery = "".join(
        "INSERT INTO track(track_uri, track_name, duration_ms, album_uri, artist_uri) VALUES('"
        + track[0][1]
        +"','"
        + track[1][1].replace("'", "")
        +"','"
        + track[2][1]
        +"','"
        + track[4][1]
        +"','"
        + track[3][1]
        +"') ON CONFLICT(track_uri) DO NOTHING;"

        for track in track_set
    )
    '''
    #print(trackquery)
    #c2.execute(artistquery)
    #c2.execute(albumquery)
    #c2.execute(trackquery)

if __name__ == '__main__':

    processes = []
    for i in range (1, 13):
        t = multiprocessing.Process(target=queries, args=(i,))
        processes.append(t)
        t.start()
    for i in range(12):
        processes[i].join()