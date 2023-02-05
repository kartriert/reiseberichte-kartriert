import functions as fu

'''
  # Programm zum Clustern von geojsons
'''
# Daten extrahieren
pfad = "reiseberichte-kartriert/travelogues/data/output/text_ner/with_url/finished/*"
data = fu.get_data(pfad)

# Dateien durchgehen
for n, d in data:
  # Terminalkonversation
  print("Neue Datei wird bearbeitet...")
  print (n)
  print("Bitte bestätigen sie die Verarbeitung der Datei (enter).")
  input()

  # weitere Daten extrahieren
  sentences = []
  #sentences = fu.get_sentences( n )

  # Daten in Form bringen
  liste, satzliste, h, fehler = fu.get_liste(d)
  print("Ortsliste wurde erstellt und wird nun geclustert...")

  # Cluster aus Daten bilden
  cluster = fu.new_cluster(liste)
  print("Clustering ist abgeschlossen, die Cluster werden nun gespeichert...")

  # Ausgabe als Datei
  fu.save_geojson(cluster, n, 'kartriert.github.io/data/cluster/', sentences)

  print("Datei wurde gespeichert. ")

