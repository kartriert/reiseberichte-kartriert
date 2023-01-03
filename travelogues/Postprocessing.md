# Documentation of the Manual Post-Correction for (Geo)JSON files


Edda: Z103519403
Jan-Philipp: Z103519506
Sarah: Z114800707 (until further notice, it has 38.000 lines...)
Solange: Z114799006
Svenja: Z114801803
Tatiana: Z69804407


## Lisa: File Z103519609

- There are many locations mentioned that are differently named in their original language. Example: "Jihlava" in the Czech Republic is called "Iglau" in the text (the German version of the name). Change the name in the GeoJSON file to the original name or leave it be?
- The GeoJSONS won't show umlaute/mutated vowels (ä, ö, ü) and ß. This leads to some location names not being recognized. Example: GeoJSON shows "pre burg" instead of "preßburg". Another Example: GeoJSON shows "olm" instead of "olmütz", which resulted in pointing to the wrong location. Is this a conversion error? If yes, could this have been prevented?
- In case of rivers, GeoJSONS will point to where the river enters another bodyy of water (e.g. sea, ocean). Will this alter the location of our cluster points too much?



