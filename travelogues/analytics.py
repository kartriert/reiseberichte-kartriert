import json
from os.path import join
import glob

sum_texts = 0
sum_locations = 0
sum_wordcount = 0
locations = []
wordcounts = []

path_travelogues_txt = 'travelogues/data/18th_century_first_quarter_corr/'
path_travelogues_geojsons = 'travelogues/data/output/text_ner/with_url/finished/'
path_julesverne_txt = 'Jules Verne/data/jules_verne_80_days_de_archive.txt'
path_julesverne_geojson = 'Jules Verne/data/jules_verne_80_days_de_archive.json'

def avg(var1, var2):
    quot = var1/var2
    return quot

def text_processing(text):
    global sum_texts 
    sum_texts+= 1
    local_wordcount = len(text.split())
    global sum_wordcount
    sum_wordcount += local_wordcount
    wordcounts.append(local_wordcount)
    return 

def json_processing(jsonfile):
    local_jsoncount = len(jsonfile["features"])
    global sum_locations
    sum_locations += local_jsoncount
    locations.append(local_jsoncount)
    return

"""
Travelogues
"""
for filename in glob.glob(join(path_travelogues_geojsons, "*.json")):
    text_id = filename.split('/')[-1].split('.')[0]
    with open(path_travelogues_txt + text_id + '.txt', "r") as infile:
        text = infile.read()
        text_processing(text)
    with open(filename, "r") as infile:
        jsonfile = json.load(infile)
        json_processing(jsonfile)

"""
Jules Verne
"""

with open(path_julesverne_txt,"r") as infile:
    text = infile.read()
    text_processing(text)

with open(path_julesverne_geojson,"r") as infile:
    jsonfile = json.load(infile)
    json_processing(jsonfile)

print("bearbeitete Texte: ")
print(sum_texts)
print("Orte pro Text (Durchschnitt): ")
print(avg(sum_locations, sum_texts))
print("Worte pro Text (Durchschnitt): ")
print(avg(sum_wordcount, sum_texts))
print(locations)
print(wordcounts)
