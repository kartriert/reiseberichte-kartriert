# Clusteranalysis

## Introduction

Goal of the clustering is the tightening and structuring of the data of each book. To reach this goal a DBSCAN-algorithm was used with the three values of latidute, longitude and sentence_idx. The formula for the distance is as followed:

math.sqrt(abs(treffer[i][0]-treffer[punkt][0])**2 + abs(treffer[i][1]-treffer[punkt][1])**2 + abs((treffer[i][2]-treffer[punkt][2])/1.1)**2)

The data will be clustered three times in the way, that the resulting clusters of the first overall clustering will be clustered again and the resulting clusters will be clustered again. 

## Data Output

The programm outputs multiple .geojson-files for each input file from inside reiseberichte-kartriert/travelogues/data/output/text_ner/with_url/finished. As the clustering the data has three forms with the following names:

1. name + '_bookpgcl' + x + '.geojson'
    -> first clustering
2. name + '_bookpgcl' + x + '_' + y + '.geojson'
    -> clustering of the clusters from first clustering
3. name + '_bookpgcl' + x + '_' + y + + '_' + z + '.geojson'
    -> clustering of the clusters of 2. results

## Bugs, Issues and Features on the run

### Bugs and Issues

- Further Modularization and Cleaning of the Code
- Finetuning of the distance math
- Pass URL to geojson

### Features

- Rebuild method to cluster distances in the Text first
- Build cluster with different values and in different ways and auto decide which clusterset is best