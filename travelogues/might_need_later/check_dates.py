import glob
import json

for file in glob.glob('/Users/sarahreb/Downloads/metadata/*.json'):
    f = open(file)
    object_dict = json.load(f)
    for l in object_dict:
        try:
            if l['label'][1]['@value'] == 'Erscheinungsdatum':
                print(l['value'])
        except TypeError:
            continue
