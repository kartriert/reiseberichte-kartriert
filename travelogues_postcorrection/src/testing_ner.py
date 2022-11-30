import re

from flair.data import Sentence
from flair.models import SequenceTagger
import spacy
from correct_ocr import single_characters, delete_specials, correct_s

# Only needed if problems with spacy.load occur
# import spacy.cli
# spacy.cli.download("de_core_news_md")


nlp = spacy.load("de_core_news_md")

# Noisy OCR :)
file: str = open('../data/test/bossmann_gvinea_1708.txt', 'r').read()
file = correct_s(file)
file = single_characters(file)
file = re.sub('aͤ', 'ä', file)
file = re.sub('uͤ', 'ü', file)
file = re.sub('oͤͤ|oͤ', 'ö', file)
file = re.sub('ey', 'ei', file)

file = delete_specials(file)
doc = nlp(file)
sents = [sent.text for sent in doc.sents]

tagger: SequenceTagger = SequenceTagger.load("dbmdz/flair-historic-ner-onb")

for sent in sents:
    sentence = Sentence(sent)
    tagger.predict(sentence)
    print(sentence.to_tagged_string())
