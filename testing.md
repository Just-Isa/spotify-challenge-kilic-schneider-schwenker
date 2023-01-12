<br><br><br>
# TESTROUTINE

> Im Ordner ***'TestRoutine'*** befindet sich eine File ***'test.py'***.
Um das Projekt richtig testen zu können, wurde die ***test.py*** so eingerichtet, dass beliebig
viele Playlists angesprochen werden können. 
><br><br>
Auch das Überprüfen einer validen submission wird gemacht. Dies funktioniert allerdings nur bei einer Angabe
von 10, 20 oder 30 Playlists.

>***Es muss ein Tunnel zur Datenbank existieren!***

```python
python test.py 10  |   python test.py 20  |  python test.py 30  
```


>Zunächst wird eine ***'test.csv'*** erstellt, in welcher die relevanten Playlistdaten aus der Datenbank zwischengespeichert werden.<br><br>
Nun werden die Daten per Logik, welche aus der RuleMining stammen in Regeln abgewandelt welche dann in der ***'testrules.csv'*** zwischengespeichert werden. <br><br>
Letztlich werden die Regeln noch angewendet, und eine endgültige File ***'testsubmissions.csv'*** erstellt.

<br>

> Falls 10, 20 oder 30 Playlists als Startparameter mitgegeben werden, wird die Submission auch auf validität überprüft.

