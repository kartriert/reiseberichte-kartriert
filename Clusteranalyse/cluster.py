import functions as fu

'''
  # Programm zum Clustern von geojsons
'''
# Daten extrahieren
pfad = "reiseberichte-kartriert/travelogues/data/output/text_ner/with_url/finished/*"
data = fu.get_data(pfad)

# Dateien durchgehen
for n, d in data:
  print("Neue Datei wird bearbeitet...")
  print (n)
  # Daten in Form bringen
  liste, satzliste, h, fehler = fu.get_liste(d)

  # Cluster aus Daten bilden
  cluster, txt = fu.new_cluster(liste)

  #Ausgabe als Textfile
  '''
  with open("reiseberichte-kartriert/Clusteranalyse/data/Text/" + n + "_cluster.txt", "w") as outfile:
    outfile.write(fu.strli(cluster))
  '''
  fu.save_geojson(liste, cluster, n)

  # Bestätigung der nächsten Datei
  input()

