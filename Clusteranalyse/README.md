# Clusteranalysis

## Introduction

Goal of the clustering is the tightening and structuring of the data of each book. To reach this goal a DBSCAN-algorithm was used with the three values of latidute, longitude and sentence_idx. The formula for the distance is as followed:
~~~
math.sqrt(abs(treffer[i][0]-treffer[punkt][0])**2 + abs(treffer[i][1]-treffer[punkt][1])**2 + abs((treffer[i][2]-treffer[punkt][2])/1.1)**2)
~~~
The data will be clustered two times in the way, that each of the resulting clusters of the first overall clustering will be clustered again. 

## Data Output

The resulting clusters will be saved in several geojson files. They will be pushed directly into the Website Repository files. The names result from the given Text name and a number and are stored in "data/cluster/". The first entry of the first cluster of each Clusterset of the texts get a foreign member named  "cluster_total" with the Total of clusterfiles for this Text.

## Workflow

The Code is splitted in the main file (cluster.py) and the functions file (functions.py). The main File shows the overall division, while the functions show the definitions.

There are  main parts:
- The extraction of the data needed especially the .geojson provided by reiseberichte/travelogues
- The clustering
- The saving of the data

### Data Extraction

First, the data for the dictionary giving the geonames will be extracted <extract_labels()>. In this file is a lokal Copy for the used geonames, so they do not need to be asked for more than once. It will be saved in the data file. For the further data extraction the finished and corrected travelogues and jules verne .geojson-files are used (found here: reiseberichte-kartriert/travelogues/data/output/text_ner/with_url/finished/* and reiseberichte-kartriert/Clusteranalyse/data/geoname_dict.json) <get_data()>. There is also an option to get the full sentences to save them in the resulting geojson <get_sentences()>, but this feature is not working properly right now (there are places not matching the resulting sentence and it is only for the Travelogues data, since there is a file for Jules Verne, that is not in use, too). It is disabled for this reason.

Once the data is extracted it will be put in the form needed: A Python-List <get_list()>. Every geojson-entry ends in an entry of the list, resulting in the following form (for a geojson with n entries):
~~~
[
    [coord0_0, coord1_0, sentenceIDX_0, place_0, geoname_0],
    [coord0_1, coord1_1, sentenceIDX_1, place_1, geoname_1],
    ...
    [coord0_n, coord1_n, sentenceIDX_n, place_n, geoname_n]
]
~~~
Both coordinates are doubles and the sentenceIDX is an integer, both found in the given geojson, while place is a string extracted from geonames with the help of the given url <get_label()> (the data from the extract_labels-file is used to spare time and prevent the program from spamming geonames). Also, it is not only the list retrieved, but further information, too. That is to say, that theese are not used right now, but are possible nice for future development. There are this three values on top of the earlier mentioned list:
- sentence index list (sli): List of all indices of the sentences mentioned in the given geojson in the same order than the other list
- highest sentence index found (h): Not just last, but compared each time a new entry is put to the list
- problems with the geojson (fehler): List of all source_labels, that could not be put to the list (e.g: they had the wrong format)

### Clustering

The next step is the clustering <new_cluster()>. The clusters are ordered from longest to shortest and show all data extracted and saved in the list earlier. As mentioned before it is a dbscan algorithm with the above specifications. However, there is a fourth value needed next to the standard list, epsilon and minPts. That is, because the algorithm offers to cluster three different dimensions and does not care about the numbers of entries in the given list. It just uses the first n entries of each point and clusters it with an given distance measurement. There are three ways implemented:
- dim = 2: euklidean distance based on the first two entries
- dim = 3: distance as shown in the introcduction based on the first three entries
- else: with every other value, an euklidean distance based on only the first entry is used

### Saving

Last part is the saving of the resulting data. For every entry in every cluster for every file there is a depending geojson file output in the form shown in Data Output. Used is the geojson library to create Feature Collections and save them as .geojsons to the data of kartriert.github.io directly. The data is saved on the backend of the Website directly: kartriert.github.io/data/cluster/ and kartriert.github.io/data/cluster_verne/.

## Bugs, Issues and Features on the run

### Bugs

- Sentence not correct

### Futere Goals

#### Next Steps
- Finetuning of the distance math

#### Long Term

- Rebuild method to cluster distances in the Text first
- Build cluster with different values and in different ways and auto decide which clusterset is best