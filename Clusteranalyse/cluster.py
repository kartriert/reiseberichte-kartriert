import json
import functions as fu

'''
  # Programm zum Clustern von geojsons
'''
# Pfade
geoname_dict_filename = "reiseberichte-kartriert/Clusteranalyse/data/geoname_dict.json"
tr_geopfade = "reiseberichte-kartriert/travelogues/data/output/text_ner/with_url/finished/*"
tr_out = "kartriert.github.io/data/cluster/"
jv_geopfad = "reiseberichte-kartriert/Jules Verne/data/jules_verne_80_days_de_archive.json"
jv_out = "kartriert.github.io/data/cluster_verne/"

# Daten extrahieren
geonames_dict = fu.extract_labels(geoname_dict_filename)
# Daten zu Jules Verne
with open(jv_geopfad, 'r', encoding='utf-8') as f:
  data = [("jules_verne_80_days_de_archive", json.load(f))]
# Daten der Travellogues
data.extend( fu.get_data(tr_geopfade) )

# Dateien durchgehen
for n, d in data:
  # Terminalkonversation
  print("")
  print("-----------------------------")
  print("Neue Datei wird bearbeitet...")
  print (n)
  print("Bitte bestätigen sie die Verarbeitung der Datei (enter).")
  input()

  # weitere Daten extrahieren
  sentences = []
  #sentences = fu.get_sentences( n )

  # Daten in Form bringen
  geonames_dict, liste, satzliste, h, fehler = fu.get_liste(d, geonames_dict)
  print("Ortsliste wurde erstellt und wird nun geclustert...")

  # Cluster aus Daten bilden
  cluster = fu.new_cluster(liste)
  print("Clustering ist abgeschlossen, die Cluster werden nun gespeichert...")

  # Ausgabe als Datei
  if (n == "jules_verne_80_days_de_archive"):
    fu.save_geojson(cluster, n, jv_out, sentences)
  else:
    fu.save_geojson(cluster, n, tr_out, sentences)

  print("Datei wurde gespeichert. ")

fu.write_dict(geonames_dict, geoname_dict_filename)
print("Alle Dateien wurden bearbeitet und geonames gespeichert. ")