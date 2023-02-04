import json
import glob
import os

import geocoder

# Enter the filename if you want to process only a single file.
file = '../might_need_later/data/Z103519403.json'
with open (file, 'r') as f:
    json_file = json.load(f)
    for feature in json_file["features"]:
        feature_label = feature["properties"]["source_label"]
        # With GeoNames URL
        if feature["properties"]["url"] == "https://www.geonames.org/None":
            g = geocoder.geonames(feature_label, key='kartriert')
            feature["properties"]["url"] = "https://www.geonames.org/" + str(g.geonames_id)

        json_dump = json.dumps(json_file, indent=4)
        with open('../data/output/text_ner/with_url/' + os.path.basename(file), 'w') as f_w:
            f_w.write(json_dump)