"""
This script aims to improve old german txt files in several ways:
DONE - Replace the old 'ſ' with 's'
NECESSARY? BUT DONE - Remove non-word characters
DONE - Reconnect words separated by line breaks
DONE - Reconnect single characters with words befor or after
- Correct common mistakes (e.g. "Teutschland")
PARTIALLY DONE - Semi-manually correct long, falsely OCRed words (criteria: number of directly succeeding consonants )

Note: the corrected texts are not usable for extraction of dates and years;
for this, a separate script should be used on the original texts

"""

import re
import os.path
import glob


def correct_s(txt):
    # Replace the old 'ſ' with 's'
    output_txt = re.sub("ſ", "s", txt)
    return output_txt


def delete_specials(txt):
    # Remove non-word characters
    """
    Fragen!
    -> Müssen die vielen Reihen an Sonderzeichen (zB an Stelle von Bildern) weg? Einzig relevant wären sie für die Stelle im Text (damit das nicht verfälscht wird)
    -> Die Sonderzeichen im Text selbst müssen nur raus, wenn dadurch Ortsnamen lesbarer werden. Einige sollten drinbleiben (Punkte, Kommas) für die Lesbarkeit (oder nicht, weil es nicht manuell durchgeguckt wird?)
    Erst Zeilenumbrüche korrigieren, dann - rauslöschen? Ausnahmen: links und rechts davon buchstaben / ein leerzeichen und buchstaben
    """
    output_txt = re.sub(r"[^a-zA-Z0-9-,üöäß.;]", " ", txt)
    return output_txt


def single_characters(txt):
    # Connect words that are separated by line breaks and connected with "-"
    txt = re.sub("(\s)([\S]+)(-\n)", r"\n\2", txt)
    # Connect single word characters with characters that come before and after
    # print(re.findall("(\w+) (\w) (\w+)", txt)) # Print all occurrences for test purposes
    txt = re.sub("(\w+) (\w) (\w+)", r"\1\2\3", txt)
    """
    Problem: Es ist unklar ob die Worte nach vorne oder hinten angebunden werden sollten! So werden sie an beide Wörter gebunden
    """
    # Connect words on one line that are divided by "-"
    txt = re.sub("(\w+)(-)(\w+)", r"\1\3", txt)
    return txt


def common_mistakes(txt):
    """
    -> Erst über NER laufen lassen, dann mit OpenRefine ältere Varianten hochdeutscher Ortsbezeichnungen anlegen (Historizität bewahren)
    """
    # Correct common mistakes
    # List of commons mistakes:
    # z -> sz, tz
    # u -> v, v -> u
    # d -> t, t -> dt
    # i -> y,j
    liste_de = ["teutschland", "teutchland", "deutchland", "deutschland"]
    # liste_au
    # liste_ch
    # liste_indien
    # etc
    for item in liste_de:
        txt = re.sub(item, "deutschland", txt)
    return txt


def correct_consonants(txt, textfile):
    """
    Still missing: Implement the case when the first found instance is right at the beginning
    Correct: Correction should only print until the line breaks
    Correct: Very last character of the text file is not being saved
    Question: Is this useful? When comparing the same text, one time correct and one time only OCRed, the former text shows 519 instanes to correct, while the latter shows 794, which is not that great of a difference.
    """
    # Semi-manual correcting of instances, where at least 5 consonants succeed each other
    # 1. Give a list of all indexes where at least 5 consonants succeed each other
    cons_list = [m.start() for m in re.finditer(
        "[bcdfghjklmnpqrstvwxyzß][bcdfghjklmnpqrstvwxyzß][bcdfghjklmnpqrstvwxyzß][bcdfghjklmnpqrstvwxyzß][bcdfghjklmnpqrstvwxyzß]+",
        txt)]
    if cons_list != []:
        print(len(cons_list))
        print(textfile,
              "will be corrected now. To correct the shown text, put in the full, corrected text. To skip, type skip. To end correction, type end. (Note: In that case, the file will still be saved normally).")
        # print(cons_list)
        # 2. Iterate over found instances
        for item in cons_list:
            print(txt[item - 5:item + 10])
            correction = input("Correction:")
            if correction == "skip":
                continue
            elif correction == "end":
                break
            else:
                # start = item-10
                # end = item+15
                txt = txt[0:item - 5] + correction + txt[item + 10:-1]
    return txt


def main():
    for textfile in glob.glob(os.path.join("testtexte", "*.*")):
        # for textfile in glob.glob(os.path.join("18th_century", "*.*")):
        with open(textfile, "r", encoding="utf-8") as f:
            txt = f.read().lower()
        # print(txt)
        txt = correct_s(txt)
        # print(txt)
        txt = delete_specials(txt)
        # print(txt)
        txt = single_characters(txt)
        # print(txt)
        # txt = common_mistakes(txt)
        # print(txt)
        # txt = correct_consonants(txt, textfile)
        # print(txt)
        # Save the result in a new folder and file
        new_textfile = textfile.split('\\')[1]
        new_textfile = os.path.join("testtexte_verbessert", new_textfile)
        # new_textfile = os.path.join("18th_century_corr1", new_textfile)
        print(new_textfile, "saved")
        with open(new_textfile, "w", encoding="utf-8") as f:
            f.write(txt)

    """
    txt = "Hallo ichſ bin hier\n\nſ\n\nſHallo\n\nHallo ſ Hallo\n"
    print(txt)
    txt = correct_s(txt)
    print(txt)
    """


main()
