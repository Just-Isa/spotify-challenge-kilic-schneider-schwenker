
# Spotify Million Playlist Challenge

>Die Spotify Million Playlist bezieht sich darauf, per datamining bzw. machinelearning Songs vorschlagen zu können, um Playlists zu vervollständigen. Hierfür gibts sowohl Algorithmische, als auch Logische Lösungswege.
  

- [Spotify Million Playlist Challenge](#spotify-million-playlist-challenge)
    - [SimilarityMatrix](#similaritymatrix)
    - [Collaborative-Filtering](#collaborative-filtering)
    - [Filtern über Trackinfos](#filtern-über-trackinfos)
    - [Assoziationsanalyse](#assoziationsanalyse)
  - [Vorgehensweise](#vorgehensweise)
    - [Daten extrahieren](#daten-extrahieren)
    - [Assoziationsregeln erstellen](#assoziationsregeln-erstellen)
    - [Assoziationsregeln Anwenden und Submission erstellen](#assoziationsregeln-anwenden-und-submission-erstellen)
- [Submissions](#submissions)
  - [Problemstellungen](#problemstellungen)
      - [Zu viele Daten](#zu-viele-daten)
  - [Lösung zu viele Daten](#lösung-zu-viele-daten)
      - [Nicht alle daten in Submission](#nicht-alle-daten-in-submission)
  - [Lösung zu nicht alle daten in Submission](#lösung-zu-nicht-alle-daten-in-submission)
      - [Anfängliche Performance-Schwierigkeiten](#anfängliche-performance-schwierigkeiten)
  - [Lösung Performance](#lösung-performance)
      - [Zugriff auf Genres der Tracks / Artists](#zugriff-auf-genres-der-tracks--artists)
  - [Lösung Extrahierung direkt aus Artist Name](#lösung-extrahierung-direkt-aus-artist-name)
    - [Problemlösungen](#problemlösungen)
      - [Lösungsansatz für zu viele Daten](#lösungsansatz-für-zu-viele-daten)
      - [Lösung für Anfängliche Performance-Schwierigkeiten](#lösung-für-anfängliche-performance-schwierigkeiten)
      - [Lösung für das Fehlen der Daten in Submissions](#lösung-für-das-fehlen-der-daten-in-submissions)
      - [Lösung für fehlende Genres in Track URI](#lösung-für-fehlende-genres-in-track-uri)
- [TESTING](#testing)
  

<br>


<a id="similarity-matrix"></a>
### SimilarityMatrix
>Track-Track similarity Matrix, in welcher Attribute von Tracks verglichen werden, und dann per Ähnlichkeitsanalyse entschieden werden kann, welche Tracks in eine Trackliste passen, um diese zu vervollständigen.

<br>

<a id="collaborative-filterin"></a>
### Collaborative-Filtering

>Collaborative-Filtering basiert auf der Annahme, dass Ähnlichkeiten zwischen den Interessen von Nutzern (hier Playlists) und Produkten (hier Tracks) existiert.
>- User-Based : Interessen des Users für Filtering verwenden
>- Item-Based : Item-Ähnlichkeit (also hier Track-Ähnlichkeit in Playlists) für das Filtern verwenden. 

<br>

<a id="trackinfo-filtern"></a>
### Filtern über Trackinfos
>Infos über die Tracks werden über die Spotify API aus den TrackURIs gezogen
>Es wird kategorisiert und so neu gegliedert - so werden sinnvoll ähnliche Tracks zusammen gruppiert
>Hierzu zählen beispielsweise Genres wie Zugehörigkeit zu Rock oder Pop, und auch die Danceability (aussagekräftiger als bspw BPM, da BPM auch für die Danceability hinzugezogen wird).

<br>


<a id="association-analysis"></a>
### Assoziationsanalyse
> Hier basierend auf dem Apriori Algorithmus, umgesetzt mit der mlxtend-library
> später ergänzt mit dem Frequent Pattern (FP) Growth Algorithmus, der ähnlich abläuft, aber für größere Datenmengen schneller abläuft.
>
> -- [Rakesh Agrawal and Ramakrishnan Srikant Fast algorithms for mining association rules][1]

Um die Daten richtig verwenden, und nach dem apriori gescheit widerspiegeln zu können, müssen diese zunächst sanitized werden.

```python
    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    baskets = df2.groupby(['playlist_id', 'track_uri'])['test'].sum().unstack().reset_index().fillna(0).set_index('playlist_id')
    baskets = baskets.applymap(encode_units)
```
> [How to use the apriori Algorithm for market basket analysis][2] -- Matt Clark
>Zunächst erstellen wir also ein neues DataFrame namens ```baskets```, in welche wir die Spalten, die wir brauchen zuweisen. In unserem Fall sind das ```playlist_id``` und ```track_uri```. <br><br>
>Nun verwenden wir die Pandas ```groupby()``` Funktion um auf beiden Spalten zu gruppieren. <br><br>
>Letztlich werden noch mit ```sum``` die Quantitäten-Spalte berechnet, mit ```unstack``` die Hierarchie nach rechts verschoben und mit ```fillna(0)``` alle nan Werte mit 0 gefüllt. 

>Als wir aber mit größeren Daten gearbeitet haben, gab es sehr lange Laufzeiten, um die Baskets zu erstellen. 
>Also haben wir nach Alternativen gesucht und den Transencoder von mlxtend entdeckt. 
>http://rasbt.github.io/mlxtend/user_guide/preprocessing/TransactionEncoder/
>der TransactionEncoder ermöglicht uns ein Dataframe aus einer Liste, welche für alle Playlist weitere Liste mit Tracks enhält, zu erstellen.
>Die Liste hätte dann diese Form: ```[[track00, .. , track0N], ... ,[trackN0, .. , trackNN]]``` nur für alle Songs von allen Playlists
```python
    te = TransactionEncoder()
    te_data = te.fit(basket).transform(basket)
    dfbasket = pd.DataFrame(te_data, columns=te.columns_)
```
>durch die Anwendung des TransactionEncoder mit der fit methode und der transform mehode wird eine 2D Liste erstellt, wo jede innere liste die information enthält, ob diese ein Träck enthält oder nicht. 
>mit hilfe von pandas erstellen wir dann damit ein dataframe.
>Daurch das Impelmentieren des TransactionEncoder ist die Laufzeit deutlich besser geworden
><br><br>Jetzt kriegen wir per unserer Apriori Implementation 
```python
itemsets = apriori(baskets, use_colnames=True, verbose=1, low_memory=False, min_support=0.01, max_len=3)
rules = association_rules(itemsets, metric="lift", min_threshold=1)
rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
```
>Regeln mit sowohl ```confidence```-Werten als auch ```lift```-Werten. ```Confidence```-Werte besagen wie "sicher" der Algorithmus ist, dass zwei Songs am besten zusammen vorkommen sollten (bzw. eben zusammen vorkommen). Per diesem Wert sind Songs dann aufeinander (oder an Songlisten) anhängbar.

## Vorgehensweise
<br>

> Vorgehensweise zum erhalten der Daten, welche für das Ergebnis (submission.csv) nötig ist.

<br>

### Daten extrahieren
>Zunächst müssen alle relevanten Daten von allen Playlists die relevant sind aus der Datenbank extrahiert werden. 
<br>
>Somit müssen die:
>- Playlist_id
>- Anzahl der Tracks
>- Kollektion von Tracks in einer Playlist
>- Position von Tracks in dieser Kollektion
>
>per Queries in eine extra CSV Datei (hier die test.csv Kaskade) übertragen werden.
<br>
<br>

### Assoziationsregeln erstellen

>Damit nun aus den in den vorherigem Schritt extrahierten Daten per Apriori Assoziationsregeln erstellt werden können, müssen die Daten in eine Datenstruktur umfunktioniert werden (aka. Pandas Dataframe). Mehr hierzu bei [Assoziationsanalyse](#assoziationsanalyse).


<br>
<br>

### Assoziationsregeln Anwenden und Submission erstellen

>Um nun letztlich die Submission File erstellen zu können, müssen die Regeln noch angewendet werden. Per Angabe der Aufgabenstellung in der Challenge, sollten pro Playlist insgesamt 500 Tracks vorkommen. Das heißt das bei einer Playlist mit 120 Songs, 380 durch das anwenden der Regeln hinzugefügt werden sollen. Auch Dopplungen von Songs sind nicht erwünscht. Nun wird also für jeden Track in jeder Playlist überprüft, ob ein Track vorkommt, welcher einen anderen Track per Assoziationsregel *"zugewiesen bekommen hat"*, und füllen die Playlists dementsprechend auf.

<br>
<br>

# Submissions

> Mit dem ersten Apriori Ansatz waren die Ergebnisse für die Submissions:
>  
![Submissions_1](/images/submission1.png)

> Mit dem Zweiten dann:

![Submissions_2](/images/submission2.png)

> Das Ergebnis zeigt also, dass es sich mehr als gelohnt hat einen weiteren Ansatz zu verfolgen.
 
<br>
<br>

## Problemstellungen


#### Zu viele Daten

>Um möglichst genaue Werte aus dem Algorithmus entnehmen zu können, macht es mehr möglichst >viele Daten auf einmal mitzugeben, bei denen vorher schon aussortiert wurde. Bereits bei < 1000 >Playlists fingen die Rechner zu rauchen an.<br>
[Lösung zu viele Daten](#loesung-zu-viele-daten)
--- 

<br>

#### Nicht alle daten in Submission

>In den Submissions scheinen Daten verloren gegangen zu sein, da bei 20.000 Playlists nur ca. 2000 in den Submissions auftauchen.<br>
[Lösung zu nicht alle daten in Submission](#loesung-nicht-alle-daten)
--- 

<br>

#### Anfängliche Performance-Schwierigkeiten

>Bei erster Implementation (und auch bei der derzeitigen) war die Performance so stark ein Problem, das nur 2-3 Playlists auf einmal verwendet werden konnten. 
[Lösung Performance](#loesung-performance)
--- 

<br>

#### Zugriff auf Genres der Tracks / Artists

>jeweilige TrackURI von Spotify enthielt einfach zugängliche Infos wie BPM, Loudness, Danceability etc; Genres waren nicht leicht zugänglich <br>
[Lösung Extrahierung direkt aus Artist Name](#loesung-genre-artist)
--- 

<br>

<br>

### Problemlösungen
<br>

#### Lösungsansatz für zu viele Daten
<a id="loesung-zu-viele-daten"></a>
> Tracks, bzw. Tracklisten, Genres zuweisen. Damit dies möglich ist, wird die [spotipy library](https://spotipy.readthedocs.io/en/2.19.0/) von Spotify selbst genutzt. Hiermit können wir bereits im Voraus Playlists/Tracklists einteilen.

--- 

<br>

#### Lösung für Anfängliche Performance-Schwierigkeiten
<a id="loesung-performance"></a>
> Erst nach genauerem spezifischen nachlesen in den Docs von mehreren Apriori Implementationen (am nennenswertesten hier [mlxtend.frequent_patterns](http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/) und [apyori](https://pypi.org/project/apyori/)), ist aufgefallen das ein ```max_len``` verwendet werden kann.


--- 

<br>

#### Lösung für das Fehlen der Daten in Submissions
<a id="loesung-nicht-alle-daten"></a>
> Dateien einzeln nacheinander aufaddieren, nicht per 'w' option (write) öffnen.

--- 

<br>


#### Lösung für fehlende Genres in Track URI
<a id="loesung-genre-artist"></a>
> Dateien wurden aus dem Artistnamen gezogen werden, hier wurden die Genres aufgelistet. Zusätzliches Problem war hierbei, dass einzelne Artists nicht erkannt wurden, dies wurde mit einer Kondition abgefangen und vorerst ignoriert.

--- 


[1]: http://www.vldb.org/conf/1994/P487.PDF
[2]: (https://practicaldatascience.co.uk/data-science/how-to-use-the-apriori-algorithm-for-market-basket-analysis)

# TESTING

> Siehe testing.md