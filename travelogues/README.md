# Subproject "Travelogues"

## The workflow
![](data/workflow.png)

## Scripts and modules


### Post-correction of (GEO)JSON files

In order to get the best results, we decided it would be beneficial to manually correct the JSON files
that contain the NER results for the travelogues. To do this in a relatively fast manner, we
created a pipeline which adds the missing URLs of the GeoNames features to the files. Since the API has a small rate limiti
(only 1000 credits per hour), a lot still has to be done a hundred percent manually.

The location results have to be corrected because the original travelogues, written in non-standardised German from the 18th century,
contain many errors. However, the NER model still managed to find a lot of entities from the noisy OCR. These instances contain
spelling errors that need to be corrected before trying to find their match on GeoNames and especially
before being displayed on our map. Additionally, historical locations were often not correctly recognised – their URLs and coordinates
need to be corrected.

The [format](https://en.wikipedia.org/wiki/GeoJSON) for the GeoJSONs.
An extended example file can be found [here](./data/output/text_ner/with_url/Z11480080X.json).
```
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "source_label": "arabien",
                "sentence_idx": 5,
                "start_position": 35,
                "end_position": 42,
                "url": "https://www.geonames.org/102358"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    "45",
                    "25"
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "source_label": "arabien",
                "sentence_idx": 13,
                "start_position": 133,
                "end_position": 140,
                "url": "https://www.geonames.org/102358"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    "45",
                    "25"
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "source_label": "haleb",
                "sentence_idx": 14,
                "start_position": 135,
                "end_position": 140,
                "url": "https://www.geonames.org/170063"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    "37.16117",
                    "36.20124"
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "source_label": "\u00a4",
                "sentence_idx": 15,
                "start_position": 77,
                "end_position": 78,
                "url": "https://www.geonames.org/None"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    null,
                    null
                ]
            }
        }
    ]
}
```
## Results
