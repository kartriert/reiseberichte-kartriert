import json
import math
import glob
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

def get_liste( geo ):
    """
        Daten aus geojson extrahieren und in Form bringen
        Input: 
            geo:    Inhalt einer geojson-Datei
        Output:
            list,   mit Listenelementen der Form:
                        [float(Coord1), float(Coord2), int(Sentence_idx), String(Source_label)]
            list,   mit Listenelementen der Form:
                        [int(Sentence_idx)]
            int,    Höchstwert von Sentence_idx
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
            # h setzen
            if (feature["properties"]["sentence_idx"] > h):
                h = feature["properties"]["sentence_idx"]
            # Dateien dem Dictionary hinzufügen
            fli.append(coor)
        except:
            # Fehlerhafte Einträge speichern
            fehler.add(feature["properties"]["source_label"])

    return fli, sli, h,  fehler


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

def strli(li):
    """
        Hilfsfunktion für die Wandling einer Liste in einen String.
        Input:
            li: list, Liste zur Umwandlung
        Output:
            String, Aus Listeninhalt erstellter String
    """
    # Beginn der Liste
    r = "[ "
    # Durchgehen der Liste
    for e in li:
        # Falls der EIntrag eine Liste ist, mache einen rekursiven Aufruf
        if type(e) == list:
            r += strli(e)
        # Sonst: Hänge Inhalt an
        else:
            r += " " + str(e) + ", "

    return r + "] "


def new_cluster(li):
    """
        Funktion zur Erstellung der Cluster
        Input:
            li: list, Liste zur Clustererstellung
        Output:
            list,   Liste mit Clustern
            String, Aus Clustern erstellter String für eine .txt Datei
    """
    # Variablen initialisieren
    re = []
    text = ""
    # 12; 6; 0.5
    text += "******************************************\n"
    # Cluster bilden
    c = cluster(li, 20, 3, 3)
    text += strli(c) 
    text += "\n"
    text += "******************************************\n"
    l1 = 0
    # Zweite Ebene Cluster erstellen
    for i in range(0, len(c)):
        re.append([c[i]])
        text += "<=============================================\n"
        l2 = 0
        xl = len(c[i])
        x = cluster(c[i], 15, 3, 3)
        text += strli(x) 
        text += "\n"
        text += "Länge vor der Clusterbildung: " + str(xl)
        text += "\n"
        # Dritte Ebene Cluster erstellen
        for j in range(0, len(x)):
            re[i].append([x[j]])
            text += "<-------------------------------------------------\n"
            l3 = 0
            yl = len(x[j])
            y = cluster(x[j], 10, 3, 3)
            text += strli(y)
            text += "\n"
            text += "Länge vor der Clusterbildung: " + str(yl)
            text += "\n"
            ## Nur zum zählen der Listeninhalte
            for l in range (0, len(y)):
                re[i][j+1].append([y[l]])
                l3 += len(y[l])
            l2 += len(y)
            text += "Länge nach der Clusterbildung: " + str(l3)
            text += "\n"
            text += "------------------------------------------------->\n"
        l1 += l2
        text += "Länge nach der Clusterbildung: " + str(l2)
        text += "\n"
        text += "=============================================>\n"

    text += "###########################################\n"
    text += str(l1)
    text += "\n"
    text += "###########################################\n"

    return re, text


'''
  # Speicherung
'''

def save_geojson (dict, cluster, name):
    """
        Funktion für die Clusterspeicherung.
        Input:
            dict:       list, mehrdimensionale Liste der Treffer
            cluster:    int, Clusterliste
            name:       String, Dateiname
    """
    # Alle Cluster durchgehen
    for i in range(0, len(cluster)):
        # Feature erstellen
        features = []
        for punkt in cluster[i][0]:
            my_point = Point((punkt[0]-180, punkt[1]-180))
            features.append(Feature(geometry=my_point, properties={"source_label": punkt[3], "sentence_idx": punkt[2]}))
        feature_collection = FeatureCollection(features)
        # Abspeichern
        with open('reiseberichte-kartriert/Clusteranalyse/data/' + name + '/' + name + '_bookpgcl' + str(i) + '.geojson', 'w') as f:
            dump(feature_collection, f)
        
        #Untercluster betrachten
        for j in range(1, len(cluster[i])):
            # Feature erstellen
            features = []
            for punkt in cluster[i][j][0]:
                my_point = Point((punkt[0]-180, punkt[1]-180))
                features.append(Feature(geometry=my_point, properties={"source_label": punkt[3], "sentence_idx": punkt[2]}))
            # Abspeichern
            feature_collection = FeatureCollection(features)
            with open('reiseberichte-kartriert/Clusteranalyse/data/' + name + '/' + name + '_bookpgcl' + str(i)+ '_' + str(j) + '.geojson', 'w') as f:
                dump(feature_collection, f)
            
            # tiefstes Untercluster betrachten
            for l in range(1, len(cluster[i][j])):
                # Features erstellen
                features = []
                for punkt in cluster[i][j][l][0]:
                    my_point = Point((punkt[0]-180, punkt[1]-180))
                    features.append(Feature(geometry=my_point, properties={"source_label": punkt[3], "sentence_idx": punkt[2]}))
                feature_collection = FeatureCollection(features)
                # Abspeichern
                with open('reiseberichte-kartriert/Clusteranalyse/data/' + name + '/' + name + '_bookpgcl' + str(i)+ '_' + str(j) + '_' + str(l) + '.geojson', 'w') as f:
                    dump(feature_collection, f)
                




def mittelwert (liste):
    """
        Hilfsfunktion für die Mittelwertberechnung.
        Input:
        liste:    list, zweidimensionale Liste der Treffer
        Output:
        int, int,   Latidute und Longitude
    """
    # Variablen initialisieren
    x = 0
    y = 0
    
    # Summen erstellen
    for e in liste:
        x += e[0]
        y += e[1]

    # Summen durch Gesamtanzahl teilen
    x = x / len(liste)
    y = y / len(liste)

    return x, y
