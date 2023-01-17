# Documentation of the Manual Post-Correction for (Geo)JSON files

Lisa: Z103519506

Svenja: Z114801803

Tatiana: Z69804407


## Lisa: File Z103519609

- There are many locations mentioned that are differently named in their original language. Example: "Jihlava" in the Czech Republic is called "Iglau" in the text (the German version of the name). Change the name in the GeoJSON file to the original name or leave it be?
- The GeoJSONS won't show umlaute/mutated vowels (ä, ö, ü) and ß. This leads to some location names not being recognized. Example: GeoJSON shows "pre burg" instead of "preßburg". Another Example: GeoJSON shows "olm" instead of "olmütz", which resulted in pointing to the wrong location. Is this a conversion error? If yes, could this have been prevented?
- In case of rivers, GeoJSONS will point to where the river enters another body of water (e.g. sea, ocean). Will this alter the location of our cluster points too much?
- Sometimes only Coordinates or only the URL is missing (due to hourly API limit?)

## Edda: File Z103519403

- In this file there were a number of false recognitions due to patterns where **special characters** (ä, ü, ö, ß, ...) where replaced with whitespaces, e. g.: rtemberg (Württemberg), m nchen (München), schlei heim (Schleißheim). I usually corrected them according to a common sense logic where I referenced other recognized geolocations and did a quick websearch.
- With regard to **state names** (e. g. Baden-Württemberg), they had sometimes been mapped to the state capital (e. g. Stuttgart) and sometimes to the category "first-order administrative division" (e. g. [Saxony](https://www.geonames.org/2842566/saxony.html)).
- **River names**: Geonames can only use one coordinate for a river. However, for some rivers there are geoname entities where the other metadata seems to be correct (e. g. [Donau](https://www.geonames.org/791630/danube-river.html)).
- Some locations have been recognized that are **typical historical house names** in Germany (e. g. Zeughaus). Since it wasn't possible without context to know, in what city the mentioned Zeughaus would be located, they will not factor into the clustering. But from context, it should be possible to map these NEs to a city.
- If there is more than one search result, how does Geonames pick one? E. g. "Hohenheim" was placed in Namibia, because the first search entry is in Namibia. Since the text mostly spoke about southern/eastern Germany, I used the german Hohenheim instead. Sometimes, alternative spelling seems to be taken into account, sometimes not?

## Sarah: File Z114800707

- Constantinopel not recognised as Konstantinopel/Istanbul.
- Words irregularly misspelled (moch a, mochh , or the like when "mochha" is meant).
- Singular feature flowing over multiple entries, e.g. two entries "beitel" and "fakih" although "beitelfakih" is meant.
- URLs only partially added to the correctly recognised locations (due to API hourly limit?).
- Nonsense entries, such as "a" or ";" -> deleted.

## Solange: File Z114799006

Since this text is about the colonization of the east coast of North America, the file contained an enormous number of ambiguous locations, such as "Ludwigsburg", "Brunswick", "New Castle", etc. This is why the manual post-correction of the file was done with the original source document at hand. Ambiguities were mostly eliminated by reading the source text and doing research on the area in question. The final document can be considered the most accurately corrected file and may therefore be useful for future research interests.

Documentation of the manual post-correction:
- Locations divided in two entries (such as "rhode island" &rarr; "rhode" and "island") were put into one
- Nonsense entries ("s", ";", "ahornbaum", "indigoblau", "berg mount", etc.) were deleted
- Entities that referred to people ("dunmore" &rarr; gouverneur of Virginia ("Earl of Dunmore")) were deleted
- Missing special characters made the identification of the correct location hard (e.g. "flu york" does not refer to "new york", but "fluß york", meaning the river York)
- Some entries refer to regions whose borders are not the same today or do not exist anymore. In those cases, the coordinates of today's location were chosen (examples: "ost florida" &rarr; today's florida, "west florida" &rarr; today's louisiana)
- Even though the coordinates of modern US were chosen for every occurence of "vereinigte Staaten von Amerika" (or similar entry), it should be kept in mind that the US only consisted of 13 colonies along the east coast at that time (source text published in 1783)
- For every occurrence of "Amerika", North America was chosen. In instances where it was clear that only the United States (excluding Canada) were meant, the coordinates for the USA were chosen.
- For every occurrence of "neu york", the source text was consulted to determine whether the state or the city (also occurring as "neu beligen") was meant
- Names with "neu-" were not always recognized by the NER. This was accurately corrected for most entries by consulting the source document ("england" vs. "neu england", "schottland" vs. "neu schottland" (Nova Scotia), "frankreich" vs. "neu frankreich" (North America), "york" vs. "neu york", etc.)
- Other ambiguities and educated guesses:
    - "neu carolina" &rarr; North Carolina (if only "carolina" occured, or "carolinen" (meaning both), North Carolina was chosen)
    - "ostindien" &rarr; Indian subcontinent
    - "westindien" &rarr; British colonies in the Caribbean
    - "neu frankreich" &rarr; North America
    - "pork" &rarr; New York, OR "pork island" in New Jersey (?)
- Some ambiguous entries solved based on educated guesses may still be incorrect (example: "st laurenz" & "st laurenzstrom" &rarr; not entirely sure if both refer to the river)
- Three locations with "null"-values remain in the final document: "lukavonika", "ludwigs bay", "cap st laurenz". These were too ambiguous and the source text was not helpful enough to determine the location.
