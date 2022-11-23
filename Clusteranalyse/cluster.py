import json
import math


'''
  # DBScan Algorithmus
'''

def dbscan(treffer, eps, minPts):
  """
    DBScan Algorithmus zur Clusterbildung eindimensionaler Daten
    Input: 
      treffer:  list, zweidimensionale Liste der Treffer
      eps:      int, Epsilonwert
      minPts:   int, minimale Anzahl an Punkten, die für Kernobjekte benötigt werden
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
          nachbarn = regionQuery(treffer, i, eps)
          # Punkt zuordnen und gegebenenfalls Cluster expandieren
          if len(nachbarn) < minPts:
              data[i]= -1
          else:
              cluster += 1
              data = expandCluster(i, nachbarn, cluster, eps, minPts, treffer, data)

  return cluster, data


def expandCluster(pkt, nachbarn, cluster, eps, minPts, treffer, data):
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
      newnachbarn = regionQuery(treffer, nachbar, eps)
      # Falls neuer Nachbar ein Kernobjekt: an Nachbarschaftsliste anhängen (und so auch expandieren)
      if len(newnachbarn) >= minPts:
        for newnachbar in newnachbarn:
          nachbarn.append(newnachbar)

    # Falls Punkt keinem Cluster angehört: Für aktuelles Cluster eintragen
    if data[nachbar] == None or data[nachbar] <= 0:
      data[nachbar] = cluster

  return data


def regionQuery(treffer, punkt, eps):
  """
    Hilfsfunktion für die DBScan-Funktion: Sucht Nachbarn eines Punktes.
    Input:
      treffer:  list, eindimensionale Liste der Treffer
      punkt:    int, Index des Punktes, dessen Nachbarn gesucht werden sollen (inklusive ihm selbst)
      eps:      int, Epsilonwert
    Output:
      list,     Integerliste der Indizes der Nachbarn
  """
  # Variablen initialisieren
  nachbarn = []

  # Abstand zu allen Punkten berechnen und gegebenenfalls in Rückgabeliste aufnehmen
  for i in range(0, len(treffer)):
      if math.sqrt(abs(treffer[i][0]-treffer[punkt][0])**2 + abs(treffer[i][1]-treffer[punkt][1])**2) <= eps:
          nachbarn.append(i)
          
  return nachbarn


def cluster (dict, eps, minp):
    """
        Hilfsfunktion für die Clusterbereinigung.
        Input:
            dict:   list, zweidimensionale Liste der Treffer
            eps:    int, Epsilonwert
            minp:   int, minimale Anzahl an Punkten, die für Kernobjekte benötigt werden
        Output:
            list,   zweidimensionale Liste der Treffer
    """
    # Clusteranalyse
    cluster, meta = dbscan(dict, eps, minp)

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


def ausgabe (final, eps):
    """
        Hilfsfunktion für die Ausgabe der Clustermittelwerte.
        Input:
            final:   list, zweidimensionale Liste der Treffer
            eps:    int, Epsilonwert
    """
    # Clusteranalyse
    final = cluster(final, eps, 4)
    print("Clusteranzahl: " + str(len(final)))

    for j in range(0, len(final)):
        print ("xxxxxxxx")
        print("Treffer in dem Cluster: " + str(len(final[j])))
        if (len(final[j]) > 100 and (eps > 3 or eps == 2)):
            print ("<-------")
            print ("Neuer Epsilonwert: " + str((int)(eps/2)))
            ausgabe(final[j], (int)(eps/2))
            print ("------->")
        elif (len(final[j]) > 100 and eps == 3):
            print ("<-------")
            print ("Neuer Epsilonwert: 2")
            ausgabe(final[j], 2)
            print ("------->")
        else:
            x, y = mittelwert(final[j])
            # Rückgängingmachung des Ausschlusses negativer Zahlen
            x = x - 180
            y = y - 180

            print ("Mittelwerte des Clusters: ")
            print (y)
            print (x)



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


'''
  # Programm zur Berechnung der Mittelwerte aus den vielversprechendsten Clustern einer Datenmenge an Geodaten
  # Große Cluster werden weiter geteilt
'''
# Erhalte Data (Dictionary aus json Datei)
f = open("../Praxismodul/Jhd18/ner-results/Z259211507.geojson")
text = json.load(f)
f.close()

# Bereinigte Daten in Liste schreiben
dict = []
for t in text["features"]:
    coor = t["geometry"]["coordinates"]
    # Verhindern negativer Werte
    coor[0] += 180
    coor[1] += 180
    # Miteinbeziehen von Mehrfachnennungen (occurance)
    for i in range (0, t["properties"]["occurrences"]):
        dict.append(coor)

ausgabe(dict, 12)
