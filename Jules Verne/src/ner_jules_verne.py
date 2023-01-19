from mordecai import Geoparser
import spacy
#spacy.cli.download("en_core_web_lg")
import re
from transformers import pipeline
import json

from flair.data import Sentence
from flair.models import SequenceTagger
import spacy
from spacy.tokens import Doc

import geocoder

#import spacy.cli
#spacy.cli.download("de_core_news_md")

txtfile = "jules_verne_80_days_de_archive.txt"

def readText (filename):
    """Imports a text ready for use.
    Returns text as a string and the clean filename as a string."""
    with open(filename, 'r', encoding="utf-8") as infile:
        content = infile.read()
        infile.close()
#        filename = filename.split('/')[2].split('.')[0]

    return content, filename

def preprocessing (gutenbergText):
    """Eliminates frontmatter and backmatter from Gutenberg corpus text"""
    body = gutenbergText.split(r"\*\*\* .*? \*\*\*")#[1]
    """Funktioniert nicht, obwohl lt. regexr exakt 2 matches"""
    body = gutenbergText.split(r"\*{3}")
    print(body)
    print(len(body))
    
    return body

def ner_mordecai(text):
    """Mordecai Python library takes different steps to achieve this result.
    First, it uses spaCy’s named entity recognition to extract place names from the text.
    Then, it uses Geonames gazetteer to find the potential coordinates for the place name.
    The final process uses neural networks to predict the country and placename from the gazetteer entries."""

    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    location = list(set([e.text for e in doc.ents if e.label_ == "GPE"]))
    for e in location:
        print(e)
    return

def ner_ger_spacy(text):
    return

def ner_ger_bert(text):
    classifier = pipeline('ner', model="fhswf/bert_de_ner")
    out = classifier(text[100:1000])
    """ wirft für 0:10000 diese Fehlermeldung:
  File "/Users/edda/Library/Python/3.7/lib/python/site-packages/transformers/models/bert/modeling_tf_bert.py", line 225, in call
    position_embeds = tf.gather(params=self.position_embeddings, indices=position_ids)
tensorflow.python.framework.errors_impl.InvalidArgumentError: Exception encountered when calling layer "embeddings" (type TFBertEmbeddings).

indices[0,595] = 595 is not in [0, 512) [Op:ResourceGather]

Call arguments received by layer "embeddings" (type TFBertEmbeddings):
  • input_ids=tf.Tensor(shape=(1, 1355), dtype=int64)
  • position_ids=None
  • token_type_ids=tf.Tensor(shape=(1, 1355), dtype=int64)
  • inputs_embeds=None
  • past_key_values_length=0
  • training=tf.Tensor(shape=(), dtype=bool)
  """
    print(out)
    print(len(out))
    
    return

def ner_ger_historic(text):
    # Downloading language model for the spacy pipeline
    nlp = spacy.load("de_core_news_md")
    # Throw document into spacy pipeline, sentencise file
    doc: Doc = nlp(text)
    sents: list = [sent.text for sent in doc.sents]

    tagger: SequenceTagger = SequenceTagger.load("dbmdz/flair-historic-ner-onb")
    
    idx = 0
    info: dict = {"type": "FeatureCollection", "features": []}

    for sent in sents:
        # Transform each sentence in the list into type Sentence for function availability
        sent = Sentence(sent)
        tagger.predict(sent)
#        sentence_mentions = sent.to_dict()
#        print(sentence_mentions)
        dummy_save_to_outfile(sent.to_tagged_string(), "_ner_results.txt")
        for entity in sent.get_spans('ner'):
            if entity.get_label("ner").value == 'LOC':
                feature_dict = {
                    "type": "Feature", "properties": {},
                    "geometry": {
                        "type": "Point", "coordinates": []
                    }
                }
                feature_dict["properties"]["source_label"] = entity.text
                print(entity.text)
                g = geocoder.geonames(entity.text, key='kartriert', featureClass='A')
                g_id = g.geonames_id
                g = geocoder.geonames(g_id, key='kartriert', method='details')
                print(g_id)
                feature_dict["geometry"]["coordinates"] = [g.lng, g.lat]
                feature_dict["properties"]["sentence_idx"] = idx
                feature_dict["properties"]["start_position"] = entity.start_position
                feature_dict["properties"]["end_position"] = entity.end_position
                try:
                    feature_dict["properties"]["url"] = "https://www.geonames.org/"+str(g_id)
                except:
                    feature_dict["properties"]["url"] = "https://www.geonames.org/None"
                info["features"].append(feature_dict)
                #info[barcode]["score"] = entity.get_label("ner").score
        idx += 1

    json_dump = json.dumps(info, indent=4)
    with open(re.sub('.txt', '.json', txtfile), 'w') as f:
        f.write(json_dump)

    return
    

def dummy_save_to_outfile(text, filename_extension):
    dummy_filename = re.sub('.txt', filename_extension, txtfile)
    with open(dummy_filename, "a", encoding="utf") as outfile:
        outfile.write(text+"\n")
    
    return

def main ():
    content, filename = readText(txtfile)
    testcontent = "Ein echter Engländer unstreitig, war Phileas Fogg vielleicht kein Londoner. Man sah ihn nie auf der Börse, noch auf der Bank, noch auf irgend einem Comtoir der City. Nie sah man in den Bassins und Doggs zu London ein Schiff, dessen Eigner Phileas Fogg gewesen wäre. In keinem Comité der Verwaltung hatte dieser Gentleman einen Platz; nie hörte man seinen Namen in einem Advocaten-Colleg, oder im Temple, in Lincoln's-Inn oder Gray's-Inn."
#    preprocessedText = preprocessing(content)
#    ner_mordecai(content)
#    ner_ger_bert(content)
    ner_ger_historic(content)
    
main()