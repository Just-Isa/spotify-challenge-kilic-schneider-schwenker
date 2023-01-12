import psycopg2 as ps
import pandas as pd
import sys
import os
import json
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from tqdm import tqdm
from mlxtend.preprocessing.transactionencoder import TransactionEncoder

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
    print("Database did not Respond! Did you start the tunnel? (aka. ssh username@login1.mi.hs-rm.de -L 9001:db.intern.mi.hs-rm.de:5432")
    sys.exit(1)

if len(sys.argv) < 2:
    print("python test.py [AMOUNT_PLAYLISTS]")
    print("Empfehlung: 10, 20, 30 Playlists.")
    print("CheckFile/Verify_Submission wird bei 10, 20, 30 mitgetestet.")
    sys.exit(1)

amountOfPlaylistsFromDB = str(sys.argv[1])
testFilePath = '../TestRoutine/results/test.csv'
ruleFilePath = "../TestRoutine/results/testrules.csv"
submissionFilePath = "../TestRoutine/results/testsubmissions.csv"
checkPathFile = "../TestRoutine/checkFiles/checkFile"+ str(sys.argv[1])+".json"



# --------------------------------------------------------------------- REMOVE PRE EXISTING TEST FILES --------------------------------------------------------------------- #

if os.path.exists(ruleFilePath):
    print("\nRemoving pre-existing rule file")
    os.remove(ruleFilePath)
    
if os.path.exists(testFilePath):
    print("Removing pre-existing test file")
    os.remove(testFilePath)
    
if os.path.exists(submissionFilePath):
    print("Removing pre-existing submission file")
    os.remove(submissionFilePath)
    
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #




# ------------------------------------------------------------ GETTING AN AMOUNT OF PLAYLISTS FROM THE DATABASE ------------------------------------------------------------ #


# -------------------- SET CLIENT ENCODING TO UTF8 BECAUSE OF WEIRD PLAYLIST NAMES -------------------- # 

c2.execute("SET client_encoding TO 'UTF8';");

# ----------------------------------------------------------------------------------------------------- # 


# -------------------- JOIN ALL RELEVANT TABLES AND GET THE DATA INTO A STRING -------------------- # 

s = f'SELECT DISTINCT * FROM (((track_pos_playlist NATURAL JOIN track) NATURAL JOIN album) NATURAL JOIN artist) NATURAL JOIN playlist WHERE playlist_id < {sys.argv[1]} ORDER BY playlist_id'

SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(s)

  
with open( testFilePath, 'w', encoding="utf-8") as f_output:
    c2.copy_expert(SQL_for_file_output, f_output)

print("\nTest.csv erfolgreich erstellt!")
# ----------------------------------------------------------------------------------------------------- # 


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #





# ---------------------------------------------------------------------- GET DOWN RULES FOR PLAYLISTS ---------------------------------------------------------------------- #
    
    
# ----------------------------- MAKE BASKET OUT OF TESTFILE FOR APRIORI ------------------------------- # 

df = pd.read_csv(testFilePath)
df = df[['playlist_id', 'track_uri']]
#df2 = df.assign(test=itemQuanity(df['track_uri']))
basket = []
playlistnb = df['playlist_id'][0]
tracks = []
print("\nVortschritt für Rules...")
for index, row in tqdm(df.iterrows()):
    if playlistnb == row['playlist_id']:
        tracks.append(row['track_uri'])
    if playlistnb != row['playlist_id']:
        basket.append(tracks)
        playlistnb = row['playlist_id']
        tracks = [row['track_uri']]
basket.append(tracks)

# ----------------------------------------------------------------------------------------------------- # 

te = TransactionEncoder()
te_data = te.fit(basket).transform(basket)
dfb = pd.DataFrame(te_data, columns=te.columns_)

itemsets = fpgrowth(dfb, use_colnames=True, verbose=0, min_support=0.001, max_len=3)

rules = association_rules(itemsets, metric="lift", min_threshold=1)
rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])

higherCnf = rules[(rules['confidence'] >= 0.6)]

rulefile = open(ruleFilePath, "w")

print("\nRules.csv wird erstellt...")
for index, rule in tqdm(higherCnf.iterrows(), total=len(higherCnf)):
    line = "".join(f'{antecedent} ' for antecedent in rule['antecedents'])
    line += "- "
    for consequent in rule['consequents']:
        line += f'{consequent} '
    line += "\n"
    rulefile.write(line)
print("\nTestrules.csv erfolgreich erstellt!")
    
    
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    
    
    
    
# ------------------------------------------------------------------------- CREATE SUBMISSION FILE ------------------------------------------------------------------------- #

# ----------------------------- GET RELEVANT PLAYLIST DATA INTO DICT  ------------------------------- # 

df = pd.read_csv(testFilePath)
df = df[['playlist_id', 'track_uri']]
playlistdict = dict()
for index, row in df.iterrows():
    if row['playlist_id'] not in playlistdict:
        playlistdict[row['playlist_id']] = [row['track_uri']]
    else:
        playlistdict[row['playlist_id']].append(row['track_uri'])
    
print("\nRules werden angewendet...")
submissions = open(submissionFilePath, "w")
submissions.write("team_info,TestTeam,test@email.com\n")
for key, val in tqdm(playlistdict.items()):
    ergline = str(key)
    lessThan50 = 0
    for rule in open(ruleFilePath, "r"):
        if lessThan50 >= 300:
            break
        acceptRule = True
        rule = rule.split("-")
        for antecedent in rule[0].strip().split(" "):
            if antecedent not in val:
                acceptRule = False
        if acceptRule is True:
            for consequent in rule[1].strip().split(" "):
                if consequent not in val and consequent not in ergline:
                    ergline += f", {consequent}"
                    lessThan50 += 1

# --------------------------------------------------------------------------------------------------- # 

                    
# -------------------- FILL PLAYLISTS THAT HAVE BELOW 500 TRACKS UNTIL THEY DO  --------------------- # 

    if lessThan50 < 300:
        for key, value in playlistdict.items():
            if lessThan50 == 300:
                break
            for track in value:
                if lessThan50 == 300:
                    break
                if track not in ergline and track not in val:
                    ergline += f", {track}"
                    lessThan50 += 1
    ergline += '\n\n'
    submissions.write(ergline)
    
print("\nTestsubmissions.csv erfolgreich erstellt!")
# --------------------------------------------------------------------------------------------------- # 

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #





# --------------------------------------------------------------------------- VERIFY SUBMISSIONS --------------------------------------------------------------------------- #
if int(sys.argv[1]) == 10 or int(sys.argv[1]) == 20 or int(sys.argv[1]) == 30:
    NTRACKS = 300
    def verify_submission(challenge_path, submission_path):
        has_team_info = False
        error_count = 0

        try:
            with open(challenge_path) as f:
                js = f.read()
            challenge = json.loads(js)
        except FileNotFoundError:
            error_count += 1
            print("Can't read the challenge set")
            return error_count

        pids = {playlist["pid"] for playlist in challenge["playlists"]}
        if len(challenge["playlists"]) != int(sys.argv[1]):
            print("Bad challenge set")
            error_count += 1

        # seed_tracks contains seed tracks for each challenge playlist
        seed_tracks = {}
        for playlist in challenge["playlists"]:
            track_uris = [track["track_uri"] for track in playlist["tracks"]]
            seed_tracks[playlist["pid"]] = set(track_uris)

        found_pids = set()

        if error_count > 0:
            return error_count

        f = open(submission_path)
        for line_no, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            if line[0] == "#":
                continue

            if has_team_info:
                fields = line.split(",")
                fields = [f.strip() for f in fields]
                try:
                    pid = int(fields[0])
                except ValueError:
                    print("bad pid (should be an integer)", fields[0], "at line", line_no)
                    error_count += 1
                    continue
                tracks = fields[1:]
                found_pids.add(pid)
                if pid not in pids:
                    print("bad pid", pid, "at line", line_no)
                    error_count += 1
                if len(tracks) != NTRACKS:
                    print(
                        "wrong number of tracks, found",
                        len(tracks),
                        "should have",
                        NTRACKS,
                        "at",
                        line_no,
                    )
                    error_count += 1
                if len(set(tracks)) != NTRACKS:
                    print(
                        "wrong number of unique tracks, found",
                        len(set(tracks)),
                        "should have",
                        NTRACKS,
                        "at",
                        line_no,
                    )
                    error_count += 1
                if seed_tracks[pid].intersection(set(tracks)):
                    print(
                        "found seed tracks in the submission for playlist",
                        pid,
                        "at",
                        line_no,
                    )
                    error_count += 1

                for uri in tracks:
                    if not is_track_uri(uri):
                        print("bad track uri", uri, "at", line_no)
                        error_count += 1

            elif line.startswith("team_info"):
                has_team_info = True
                tinfo = line.split(",")
            else:
                print("missing team_info at line", line_no)
                error_count += 1

        if len(found_pids) != len(pids):
            print(
                "wrong number of playlists, found", len(found_pids), "expected", len(pids)
            )
            error_count += 1

        return error_count


    def is_track_uri(uri):
        fields = uri.split(":")
        return (
            len(fields) == 3
            and fields[0] == "spotify"
            and fields[1] == "track"
            and len(fields[2]) == 22
        )
        
    errors = verify_submission(checkPathFile, submissionFilePath)
    if errors == 0:
        print(
            "\nSubmission is OK! Remember to gzip your submission before submitting it to the challenge."
        )
    else:
        print(
            "Your submission has",
            errors,
            "errors. If you submit it, it will be rejected.",
        )
else:
    print("\nKeine 10, 20 oder 30 Playlists. Keine Validation!")

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
