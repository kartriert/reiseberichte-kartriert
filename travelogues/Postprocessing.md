# Documentation of the Manual Post-Correction for (Geo)JSON files




Jan-Philipp: Z103519506

Sarah: Z114800707 (until further notice, it has 38.000 lines...)

Solange: Z114799006

Svenja: Z114801803

Tatiana: Z69804407


## Lisa: File Z103519609

- There are many locations mentioned that are differently named in their original language. Example: "Jihlava" in the Czech Republic is called "Iglau" in the text (the German version of the name). Change the name in the GeoJSON file to the original name or leave it be?
- The GeoJSONS won't show umlaute/mutated vowels (ä, ö, ü) and ß. This leads to some location names not being recognized. Example: GeoJSON shows "pre burg" instead of "preßburg". Another Example: GeoJSON shows "olm" instead of "olmütz", which resulted in pointing to the wrong location. Is this a conversion error? If yes, could this have been prevented?
- In case of rivers, GeoJSONS will point to where the river enters another body of water (e.g. sea, ocean). Will this alter the location of our cluster points too much?

## Edda: File Z103519403

- In this file there were a number of false recognitions due to patterns where **special characters** (ä, ü, ö, ß, ...) where replaced with whitespaces, e. g.: rtemberg (Württemberg), m nchen (München), schlei heim (Schleißheim). I usually corrected them according to a common sense logic where I referenced other recognized geolocations and did a quick websearch.
- With regard to **state names** (e. g. Baden-Württemberg), they had sometimes been mapped to the state capital (e. g. Stuttgart) and sometimes to the category "first-order administrative division" (e. g. [Saxony](https://www.geonames.org/2842566/saxony.html)).
- **River names**: Geonames can only use one coordinate for a river. However, for some rivers there are geoname entities where the other metadata seems to be correct (e. g. [Donau](https://www.geonames.org/791630/danube-river.html)).
- Some locations have been recognized that are **typical historical house names** in Germany (e. g. Zeughaus). Since it wasn't possible without context to know, in what city the mentioned Zeughaus would be located, they will not factor into the clustering. But from context, it should be possible to map these NEs to a city.
- If there is more than one search result, how does Geonames pick one? E. g. "Hohenheim" was placed in Namibia, because the first search entry is in Namibia. Since the text mostly spoke about southern/eastern Germany, I used the german Hohenheim instead. Sometimes, alternative spelling seems to be taken into account, sometimes not?

## Sarah: File Z114800707

- Constantionpel not recognised as Konstantinopel/Istanbul.
- Words irregularly misspelled (moch a, mochh , or the like when "mochha" is meant).
- Singular feature flowing over multiple entries, e.g. two entries "beitel" and "fakih" although "beitelfakih" is meant.
- URLs only partially added to the correctly recognised locations (due to API hourly limit?).
- Nonsense entries, such as "a" or ";" -> deleted.