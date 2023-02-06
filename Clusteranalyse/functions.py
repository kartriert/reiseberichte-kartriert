import json
import geocoder
import math
import glob
import nltk
nltk.download('punkt')
from geojson import Feature, Point, FeatureCollection, dump


'''
  # Datenmanagement
'''

def get_data( allgem_pfad ):
    """
        Funktion zum Einlesen von Dateinamen und -inhalten eines Ordners
        Input: 
            allgem_pfad:    Pfad zu Ordner mit Zieldateien
        Output:
            array,  mit Tupeln: (Dateiname, Dateiinhalt). Dateiname ist ohne Endung
    """
    # Variablen initialisieren
    data = []
    # Dateien durchgehen
    for pfad in glob.glob(allgem_pfad):
        f = open(pfad)
        # Daten hinzufügen
        data.append((pfad.split("/")[-1].split(".")[0], json.load(f)))
        f.close()
    
    return data


def get_sentences( name ):
    """
        Text in Sätze einteilen und abspeichern
        Input: 
            name:   Name für Dateipfad
        Output:
            list,   Sätze
    """
    # Variablen initialisieren
    if (name == "jules_verne_80_days_de_archive"):
        pfad = "reiseberichte-kartriert/Jules Verne/data/jules_verne_80_days_de_archive.txt"
    else:
        pfad = "reiseberichte-kartriert/travelogues/data/18th_century_first_quarter_corr/" + name + ".txt"

    file: str = open(pfad, 'r').read()
    sents = nltk.sent_tokenize(file, language='german')
    
    return sents
    
    
def get_label( url, gnl ):
    """
        Daten aus URL extrahieren
        Input: 
            url:    geonames URL zu Ort
            gnl:    bereits angelegte geonames Liste
        Output:
            String, Ortsname
            dict,   aktualisierte Liste
    """
    # Bearbeite URL
    g_id = url.split("/")
    
    # Extrahiere gegebenenfalls Daten
    if not g_id[-1] in gnl:
        gnl[g_id[-1]] = geocoder.geonames(g_id[-1], method='details', key='kartriert').address

    return gnl[g_id[-1]], gnl
    


def get_liste( geo, gnl ):
    """
        Daten aus geojson extrahieren und in Form bringen
        Input: 
            geo:    Inhalt einer geojson-Datei
            gnl:    bereits angelegte geonames Liste
        Output:
            dict,   aktualisierte Liste
            list,   mit Listenelementen der Form:
                        [float(Coord1), float(Coord2), int(Sentence_idx), String(Source_label)]
            list,   mit Listenelementen der Form:
                        [int(Sentence_idx)]
            int,    genutzter Höchstwert von Sentence_idx
            set,    Source_label aller Fehlerhaften Einträge
    """
    # Variablen initialisieren
    fli = []
    sli = []
    fehler = set()
    h = 0

    # Einträge durchgehen
    for feature in geo["features"]:
        coor = feature["geometry"]["coordinates"]
        try:
            # Daten sammeln
            # Verhindern negativer Werte
            coor[0] = float(coor[0]) + 180
            coor[1] = float(coor[1]) + 180
            coor.append(int(feature["properties"]["sentence_idx"]))
            sli.append([int(feature["properties"]["sentence_idx"])])
            coor.append(feature["properties"]["source_label"])
            l, gnl = get_label(feature["properties"]["url"], gnl)
            coor.append(l)
            coor.append(feature["properties"]["url"])
            # h setzen
            if (feature["properties"]["sentence_idx"] > h):
                h = feature["properties"]["sentence_idx"]
            # Dateien dem Dictionary hinzufügen
            fli.append(coor)
        except:
            # Fehlerhafte Einträge speichern
            fehler.add(feature["properties"]["source_label"])

    return gnl, fli, sli, h,  fehler



'''
  # DBScan Algorithmus
'''

def dbscan(treffer, eps, minPts, dim):
  """
    DBScan Algorithmus zur Clusterbildung eindimensionaler Daten
    Input: 
      treffer:  list, zweidimensionale Liste der Treffer
      eps:      int, Epsilonwert
      minPts:   int, minimale Anzahl an Punkten, die für Kernobjekte benötigt werden
      dim:      int, Dimension von Treffer (Einträge müssen mindestens dim-lang sein)
                ! maximale Dimension ist momentan 3
                ! Default (bei dim != 2 oder 3) wird der erste Eintrag des Listeneintrags von treffer genommen
    Output:
      int,      Anzahl der Cluster
      list,     Zuordnung der Cluster entsprechend der Trefferliste:
                  -1: (vorläufiges) Rauschen
                  0:  Besucht, aber nicht zugeordnet
                  1..:Clusternummer
  """
  # Variablen initialisieren
  data = [None] * len(treffer)
  cluster = 0

  # Überprüfung aller Punkte
  for i in range(0, len(treffer)):
      # Falls Punkt noch nicht besucht wurde:
      if data[i] == None:

          # Punkt als besucht eintragen
          if data[i] == None:
              data[i] = 0
          # Nachbarn heraussuchen
          nachbarn = regionQuery(treffer, i, eps, dim)
          # Punkt zuordnen und gegebenenfalls Cluster expandieren
          if len(nachbarn) < minPts:
              data[i]= -1
          else:
              cluster += 1
              data = expandCluster(i, nachbarn, cluster, eps, minPts, treffer, data, dim)

  return cluster, data


def expandCluster(pkt, nachbarn, cluster, eps, minPts, treffer, data, dim):
  """
    Hilfsfunktion für die DBScan-Funktion: Expandiert ein Cluster.
    Input:
      pkt:      int, Index des Kernobjekts
      nachbarn: list, Indizes der Nachbarn des Kernobjekts
      cluster:  aktuelle Clusternummer
      eps:      int, Epsilonwert
      minPts:   int, minimale Anzahl an Punkten, die für Kernobjekte benötigt werden
      treffer:  list, eindimensionale Liste der Treffer
      data:     list, eindimensionale Liste der Metadaten in Abhängigkeit der Trefferliste:
                  -1: (vorläufiges) Rauschen
                  0:  Besucht, aber nicht zugeordnet
                  1..:Clusternummer
      dim:      int, Dimension von Treffer (Einträge müssen mindestens dim-lang sein)
                ! maximale Dimension ist momentan 3
                ! Default (bei dim != 2 oder 3) wird der erste Eintrag des Listeneintrags von treffer genommen
    Output:
      list,       Zuordnung der Cluster entsprechend der Trefferliste
  """
  # Punkt dem Cluster zuordnen
  data[pkt] = cluster

  # Alle Nachbarn durchgehen
  for nachbar in nachbarn:
    # Falls Punkt noch nicht besucht wurde
    if data[nachbar] == None:

      # Punkt als besucht eintragen und Nachbarn herraussuchen
      data[nachbar] = 0
      newnachbarn = regionQuery(treffer, nachbar, eps, dim)
      # Falls neuer Nachbar ein Kernobjekt: an Nachbarschaftsliste anhängen (und so auch expandieren)
      if len(newnachbarn) >= minPts:
        for newnachbar in newnachbarn:
          nachbarn.append(newnachbar)

    # Falls Punkt keinem Cluster angehört: Für aktuelles Cluster eintragen
    if data[nachbar] == None or data[nachbar] <= 0:
      data[nachbar] = cluster

  return data


def regionQuery(treffer, punkt, eps, dim):
  """
    Hilfsfunktion für die DBScan-Funktion: Sucht Nachbarn eines Punktes.
    Input:
      treffer:  list, zweidimensionale Liste der Treffer
      punkt:    int, Index des Punktes, dessen Nachbarn gesucht werden sollen (inklusive ihm selbst)
      eps:      int, Epsilonwert
      dim:      int, Dimension von Treffer (Einträge müssen mindestens dim-lang sein)
                ! maximale Dimension ist momentan 3
                ! Default (bei dim != 2 oder 3) wird der erste Eintrag des Listeneintrags von treffer genommen
    Output:
      list,     Integerliste der Indizes der Nachbarn
  """
  # Variablen initialisieren
  nachbarn = []

  # Abstand zu allen Punkten berechnen und gegebenenfalls in Rückgabeliste aufnehmen
  for i in range(0, len(treffer)):
      if dim == 2:
        if math.sqrt(abs(treffer[i][0]-treffer[punkt][0])**2 + abs(treffer[i][1]-treffer[punkt][1])**2) <= eps:
          nachbarn.append(i)
      elif dim == 3: 
        if math.sqrt(abs(treffer[i][0]-treffer[punkt][0])**2 + abs(treffer[i][1]-treffer[punkt][1])**2 + abs((treffer[i][2]-treffer[punkt][2])/1.1)**2) <= eps:
          nachbarn.append(i)
      else: 
        if abs(treffer[i][0]-treffer[punkt][0]) <= eps:
          nachbarn.append(i)
          
  return nachbarn



'''
  # Clusterbildung
'''

def cluster (dict, eps, minp, dim):
    """
        Hilfsfunktion für die Clusterbereinigung.
        Input:
            dict:   list, zweidimensionale Liste der Treffer
            eps:    int, Epsilonwert
            minp:   int, minimale Anzahl an Punkten, die für Kernobjekte benötigt werden
            dim:    int, Dimension von Treffereinträgen (Einträge müssen Listen der Länge dim sein)
                    ! maximale Dimension ist momentan 3
                    ! Default (bei dim != 2 oder 3) wird der erste Eintrag des Listeneintrags von treffer genommen
        Output:
            list,   zweidimensionale Liste der Treffer
    """
    # Clusteranalyse
    cluster, meta = dbscan(dict, eps, minp, dim)

    # größtes Cluster heraussuchen
    # Variablen initialisieren
    final = []
    for i in range(0,cluster):
        final.append([])

    # Einem Cluster zugeordnete Treffer in nach Cluster geordnete Liste einsortieren
    for i in range(0, len(dict)):
        if meta[i] >= 1:
            z = meta[i]-1
            final[z].append(dict[i])

    # Liste nach Trefferanzahl sortieren
    final = sorted(final, key=lambda e: len(e), reverse=True)

    return final


def new_cluster(li):
    """
        Funktion zur Erstellung der Cluster
        Input:
            li: list, Ortsliste zur Clustererstellung
        Output:
            list,   Liste mit Clustern
    """
    # Variablen initialisieren
    re = []

    # Cluster bilden
    c = cluster(li, 20, 3, 3)
    # Zweite Ebene Cluster erstellen
    for i in range(0, len(c)):
        re.extend(cluster(c[i], 15, 3, 3))

    return re



'''
  # Speicherung
'''

def save_fc(filename, features):
    """
        Hilfsfunktion zur Speicherung  von Feature-Collections in geojsons.
        Input:
            filename:    String, Pfad und Name der resultierenden Datei
            features:    FeatureCollection, Inhalte der Datei
    """
    with open(filename + '.geojson', 'w') as f:
            dump(features, f)


def save_geojson (cluster, name, pfad, sentences = []):
    """
        Funktion für die Clusterspeicherung.
        Input:
            cluster:    int, Clusterliste
            name:       String, Dateiname
            pfad:       String, Pfad zum Ordner, in den die Clustergespeichert werden
            sentences:  list, Sätze mit den Sentence IDs
    """
    zifname = 0

    # Alle Cluster durchgehen
    for i in range(0, len(cluster)):
        # Feature erstellen
        features = []
        for punkt in cluster[i]:
            my_point = Point((punkt[0]-180, punkt[1]-180))
            if (sentences != []):
                features.append(Feature(geometry=my_point, properties={"source_label": punkt[3], "geonames_label": punkt[4], "url": punkt[5], "sentence_idx": punkt[2], "sentence": sentences[punkt[2]]}))
            else:
                features.append(Feature(geometry=my_point, properties={"source_label": punkt[3], "geonames_label": punkt[4], "url": punkt[5], "sentence_idx": punkt[2]}))
        feature_collection = FeatureCollection(features)

        # Abspeichern
        zifname += 1
        if (zifname == 1):
            fc0 = feature_collection
        else:
            save_fc(pfad + name + '_cl' + str(zifname), feature_collection)
    # Erster Eintrag im ersten Cluster erhält Gesamtanzahl der Cluster dieses Textes
    fc0[0]["properties"]["cluster_total"] = zifname
    save_fc(pfad + name + '_cl' + str(1), fc0)


def write_dict(data, pfad):
    """
        Funktion zum Abspeichern eines Lexikon (dictionary)
        Input:
            data:   dict, Lexikon der Verbindungen zwischen geonamesURL (nur Ziffernteil) und dortigem Namen
            pfad:   String, an dem das dictionary abgespeichert wird
    """
    with open(pfad, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def extract_labels(pfad):
    """
        Funktion zum lesen eines Lexikon (dictionary)
        Input:
            pfad:   String, an dem das dictionary abgespeichert wird
        Output:
            dict,   Lexikon der Verbindungen zwischen geonamesURL (nur Ziffernteil) und dortigem Namen
    """
    try:
        with open(pfad, 'r', encoding='utf-8') as f:
            geoname_dict = json.load( open( pfad ) )
    except FileNotFoundError:
        geoname_dict = {}
    return geoname_dict

