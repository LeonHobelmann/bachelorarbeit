# Bachelorarbeit „Ethische Herausforderungen in der Bildgenerierung am Beispiel von Midjourney“ - Daten

## Autor

**Autor:**<br>
Leon Hobelmann
<br>B.Sc. Wirtschaftsinformatik

**Betreuerin:**<br>
[Prof. Dr. Birte Malzahn](https://www.htw-berlin.de/hochschule/personen/person/?eid=8589)
<br>Kontaktadresse: Birte.Malzahn@HTW-Berlin.de

**Institution:**<br>
Hochschule für Technik und Wirtschaft Berlin <br>
Fachbereich 4 

## Datensatz
Es wurde eine empirsische Umfrage durchgeführt. 110 Personen haben an der Umfrage Teilgenommen. 

**Sprache:** Deutsch.

## Datenzugriff und Datenschutz

Daten wurden selbst erhoben. Datensatz ist bereinigt unter folgendem Link abrufbar.
 LIZENZ?
Die Umfrage war freiwillig und erst für Personen ab 18 Jahren zugelassen.
Alle Teilnehmer haben die Teilnahmebedingungen bestätigt.
Es wurden E-Mail Adressen der Teilnehmer (Freiwillige Angabe) gespeichert, um Teilnehmer nach 
der Auswertung über Ergebnis der Umfrage zu informieren. 
Die E-Mail Adressen werden nach Versand der Ergebnisse gelöscht. 
Die E-Mail Adressen wurden getrennt zu den Antwortern erhoben. Eine Rückschluss ist ausgeschlossen. 


## Zeitraum

Die Umfrage wurde zwischen dem 28.06.2025 und dem 06.07.2025 durchgeführt.
Die Datenanalyse fand ab dem 07.07.2025 statt.

## Angewendete Software

* Die Rohdaten: Microsoft Excel <https://www.microsoft.com/de-de/microsoft-365/excel?market=de>
* Die Auswertung: Python 3.12 <https://www.python.org/>
* Die Entwicklungsumgebung:  PyCharm <https://www.jetbrains.com/pycharm/>

## Datenformate und -größe

Interviews liegen in folgenden Formaten vor:

* Video-Dateien (.mp4): 100 MB pro Interview,
* die Transkripte (.pdf): 5 MB (alle zusammen),
* Analyse als QualCoder Datei (.qda): 3 MB

## Qualitätssicherungsmaßnahmen

Manuelle Prüfung und Korrektur der Transkripte, insbesondere:

* Korrigieren von Worten oder Absätzen, als diese falsch transkribiert worden sind;
* Korrigieren der Zuordnung des Gesprochenen;
* Ergänzen von Interjektionen (Ausruf- und Empfindungsworten).

## Ordnerstruktur & Dateibennenungskonvention

Für allen Dateien:

- X -- Nummer des Interviews
- JJJJ-MM-TT -- Datum der Dateierstellung

**Ordner:** Aufzeichnungen
`Int[X]_Aufzeichnung_JJJJ-MM-TT.mp4`

- unbearbeitete Videodaten aus den Interviews

**Ordner:** Transkripte
`Int[X]_Transkript_[roh/fertig]_JJJJ-MM-TT.pdf`

- rohe und manuell korrigierte Transkripte (2 Dateien pro Interview)
- roh -- von f4x generierte Textdatei
- fertig -- manuell korrigierte Version der rohen Datei

**Ordner:** wisskommprojekt.qda

- von QualCoder generierter Ordner mit Analysedaten
