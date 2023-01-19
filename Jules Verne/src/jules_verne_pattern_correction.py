import json

with open ("../data/jules_verne_80_days_de_archive.json", "r") as infile:
    data = json.load(infile)

def set_url(json, url):
    json["properties"]["url"] = url
    return

def set_coordinates(json, long, lat):
    if long:
        json["geometry"]["coordinates"] = [long,lat]
    else:
        json["geometry"]["coordinates"] = [None,None]
    return

for i in data["features"]:

    #replace wrongly reconized patterns
    if i["properties"]["source_label"] == "Bombay":
        set_url(i, "https://www.geonames.org/1275339")
        set_coordinates(i,"72.88261","19.07283")

    elif i["properties"]["source_label"] == "Calcutta":
        set_url(i, "https://www.geonames.org/1275004")
        set_coordinates(i,"88.36304","22.56263")

    elif i["properties"]["source_label"] == "Dover":
        set_url(i, "https://www.geonames.org/2651048")
        set_coordinates(i,"1.31257","51.12598")

    elif i["properties"]["source_label"] == "Turin":
        set_url(i, "https://www.geonames.org/3165524")
        set_coordinates(i,"7.68682","45.07049")
    
    elif i["properties"]["source_label"] == "London":
        set_url(i, "https://www.geonames.org/2643743")
        set_coordinates(i,"-0.12574","51.50853")
    
    elif i["properties"]["source_label"] == "Amerika":
        set_url(i, "https://www.geonames.org/6255149")
        set_coordinates(i,"-100.54688","46.07323")

    elif i["properties"]["source_label"] == "San Francisco":
        set_url(i, "https://www.geonames.org/5391959")
        set_coordinates(i,"-122.41942","37.77493")

    elif i["properties"]["source_label"] == "Liverpool":
        set_url(i, "https://www.geonames.org/2644210")
        set_coordinates(i,"-2.97794","53.41058")
    
    #delete wrongly recognized entities

    elif i["properties"]["source_label"] == "Doggs":
        set_url(i, "https://www.geonames.org/None")
        set_coordinates(i)

    elif i["properties"]["source_label"] == "Fogg":
        set_url(i, "https://www.geonames.org/None")
        set_coordinates(i)

with open ("../data/jules_verne_80_days_de_archive.json", "w") as outfile:
    json.dump(data, outfile)