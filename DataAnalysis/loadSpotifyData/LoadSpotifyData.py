import psycopg2 as ps
import sys

connectionex = {
    "host": "localhost",
    "port": "9001",
    "database": "pschn004_Spotify",
    "user": "pschn004",
    "password": "test"}
try:
    cnx2 = ps.connect(**connectionex)
    c2 = cnx2.cursor()
except:
    print("didnt work fella")
    sys.exit(1)

c2.execute("SET client_encoding TO 'UTF8';");
s = 'SELECT DISTINCT * FROM (((track_pos_playlist NATURAL JOIN track) NATURAL JOIN album) NATURAL JOIN artist) NATURAL JOIN playlist WHERE playlist_id > 800000 AND playlist_id <= 1000000 ORDER BY playlist_id'
#s = 'SELECT DISTINCT * FROM track_pos_playlist WHERE playlist_id <1000 ORDER BY playlist_id, track_pos'
SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(s)

with open('E:\\Data Science\\Spotify-Challenge-Kilic-Schneider-Schwenker\\DataAnalysis\\testfiles\\200.000 Schritte\\test5.csv', 'a', encoding="utf-8") as f_output:
    c2.copy_expert(SQL_for_file_output, f_output)
