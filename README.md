# Reiseberichte karTRIERt (Mapping Travelogues)

## A repository for code and data developed in the Projektseminar "Praxis der Digital Humanities" (WiSe 2022/23) at Trier University

### Introduction to the project and its ideas

During the course of this semester, we, a group of seven students, are to create, execute and wrap up
a self-chosen project in the field of Digital Humanities. 
As basis for the project "Reiseberichte karTRIERt", we chose the process of transforming
mentions of locations in texts to an actual map.

We are using two data repositories for this:

First, we chose the [Travelogues project](https://www.travelogues-project.info) and their corpus of
travel reports from the 18th century (they also provide data from the 16th and 17th century; reasons for choosing only one century
are explained in our ["Travelogues" section](https://kartriert.github.io/travelogues.html) on our website).
[Link to our Travelogues subproject](travelogues/README.md)

Second, we built a corpus out of Jules Verne's ["Around the World in Eighty Days"](https://en.wikipedia.org/wiki/Around_the_World_in_Eighty_Days) from 1873. Here, we wanted to be able to compare our "Travelogues" results - which were prone to mistakes, due to its automatic OCR and the use of old German - with a more accessible and correct text publication. More on this on our ["Korpus" section](https://kartriert.github.io/ueber_projekt.html) on our website.
[Link to our Jules Verne subproject](Jules_Verne/README.md)

### Bringing the locations on to the map

Our first step in visualizing the locations was to find them inside the texts. Since they were too long to filter through manually, we used a [Named Entity Recognition model for historic German](https://huggingface.co/dbmdz/flair-historic-ner-onb) and corrected the resulting json files semi-autimatically. More on the corresponding page on [our website](https://kartriert.github.io/NER.html).

In between the json files with the location data and the map, we wanted to bring a cluster analysis. This was to help eliminate mistakes made by incorrect OCR and resulting incorrect NER. More on this on [our website](https://kartriert.github.io/clustering.html).
[Link to our cluster analysis subproject](Clusteranalyse/README.md)

Lastly, we had to build a website and integrate the map and the data onto it. For our map, we used [Github Pages](https://pages.github.com/) to build a static website. The map was then realized with Leaflet. You can find more information on our website in the ["Website"](https://kartriert.github.io/website.html) and ["Map"](https://kartriert.github.io/karte_text.html) sections.
[Link to our website subproject](https://github.com/kartriert/kartriert.github.io/blob/main/Readme.txt)
[Link to our map subproject](Leaflet-Test/README.md)

### Subprojects and their workflows

#### [Travelogues](travelogues/README.md)
#### [Jules Verne](Jules_Verne/README.md)
#### [Cluster Analysis](Clusteranalyse/README.md)
#### [Map](Leaflet-Test/README.md)
#### [Website](https://github.com/kartriert/kartriert.github.io/blob/main/Readme.txt)
