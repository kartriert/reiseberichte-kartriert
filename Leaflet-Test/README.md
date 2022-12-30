Test-Karte mit Travelogues-Daten zum 16. Jahrhundert. Nicht auf Github-Pages ausführbar, da es sich durch das CGI-Skript in Python um eine dynamische Webseite handelt.
Zum Ausführen offline muss ein Http-Server im lokalen Leaflet-Test-Verzeichnis gestartet werden. Nicht vergessen, dass dabei die --cgi Option aktiviert sein muss.

30.12.2022:
- Massenimport der Publikationsdaten für Timeline-Slider implementiert
- Massenimport der Titel für Layerauswahl implementiert
- Sortierung und Gruppierung der Layer nach Datum zur korrekten Präsentation auf dem Zeitstrahl (nur ein Punkt pro Jahr auf dem Slider)
- Massenimport über CGI systemneutral gestaltet
- Zufällige Farben für Marker
