# Clusteranalysis

## Introduction

Goal of the clustering is the tightening and structuring of the data of each book. To reach this goal a DBSCAN-algorithm was used with the three values of latidute, longitude and sentence_idx. The formula for the distance is as followed:

math.sqrt(abs(treffer[i][0]-treffer[punkt][0])**2 + abs(treffer[i][1]-treffer[punkt][1])**2 + abs((treffer[i][2]-treffer[punkt][2])/1.1)**2)

The data will be clustered two times in the way, that the resulting clusters of the first overall clustering will be clustered again. 

## Data Output

The resulting clusters will be saved in several geojson files. They will be pushed directly into the Website Repository files. The names result from the given Text name and a number and are stored in "data/cluster/". The first entry of the first cluster of each Clusterset of the texts get a foreign member named  "cluster_total" with the Total of clusterfiles for this Text.

## Bugs, Issues and Features on the run

### Bugs and Issues

- !Pass URL to geojson

- Further Modularization and Cleaning of the Code
- Finetuning of the distance math

### Features

- Rebuild method to cluster distances in the Text first
- Build cluster with different values and in different ways and auto decide which clusterset is best