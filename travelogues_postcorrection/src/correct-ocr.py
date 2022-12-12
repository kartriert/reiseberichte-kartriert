"""
This script aims to improve old german txt files in several ways:
DONE - Replace the old 'ſ' with 's'
DONE - Remove non-word characters
DONE - Reconnect words separated by line breaks
DONE - Reconnect single characters with words befor or after
DONE - Correct common mistakes (e.g. "Teutschland")
DONE - Semi-manually correct long, falsely OCRed words (criteria: number of directly succeeding letters)

Note: the corrected texts are not usable for extraction of dates and years since some of the numbers might get edited out;
for this, a separate script should be used on the original texts

"""

import re
import os.path
import glob

def correct_s(txt):
    # o -> º
    output_txt = re.sub("º", "o", txt)
    # ë, č # These shouldn't be of much importance
    output_txt = re.sub("ë", "e", txt)
    output_txt = re.sub("č", "c", txt)
    # Replace the old 'ſ' with 's'
    output_txt = re.sub("ſ", "s", txt)
    # Replace aͤ, oͤ, uͤ with ä, ö, ü
    return output_txt

def single_characters(txt):
    # Connect words that are separated by line breaks and connected with "-"
    txt = re.sub("(\s)([\S]+)(-\n)", r"\n\2", txt)
    # Connect single word characters with characters that come before and after
    txt = re.sub("(\w+) (\w) (\w+)", r"\1\2\3", txt)
    # Connect "-" with characters that come before and after, but only if they are letters
    txt = re.sub("(\w+) (-) (\w+)", r"\1\2\3", txt)
    return txt

def delete_specials(txt):
    # Remove non-word characters / all characters except the following
    txt = re.sub("[^a-z0-9\n,üöäß.; ]", " ", txt)
    # Note: Do not delete "-" in between letters, since it can impair the NER's ability to find places (Example: Ost-Indien / Ostindien)
    return txt

def common_mistakes(txt):
    # Correct common mistakes
    # List of commons mistakes:
    # z -> sz, tz # Not usable, since too many instances of "sz" and "tz" are already correct
    # u -> v, v -> u # Not usable without context, since too many instances of "v" and "u" are already correct
    # d -> t, t -> dt, k -> c # Also not really usable
    # f -> s (zB Aufenthalt) # Also not
    # ss -> ff # Has a few instances where it should be corrected, but alos many where it shouldn't
    # t -> th
    txt = re.sub('th', 't', txt)
    # sich -> fich
    # sie -> fie
    txt = re.sub('fich', 'sich', txt)
    txt = re.sub('fie', 'sie', txt)
    # s, ss -> f, ff
    # sei -> fei, fey
    txt = re.sub('ey', 'ei', txt)
    txt = re.sub('fei', 'sei', txt)
    # in -> jn # Also helps find "Indien" better
    txt = re.sub('jn', 'in', txt)
    # Countries: DE
    txt = re.sub('teutschland', 'deutschland', txt)
    # More common country spelling mistakes...?
    return txt

def correct_consonants(txt, textfile):
    """
    How useful is this? One text has over 1600 found instances that must then all be corrected; however, many texts also only have 20-50
    """
    # Semi-manual correction of instances, where at least 5 consonants succeed each other
    
    # Give a list of all indexes where at least 19 letters succeed each other
    letter_list = [m.start() for m in re.finditer("\w{19}\w*", txt)]
    # Save the length of the list to use as indicator later
    maxx = len(letter_list)
    print(maxx)
    # Initiate list index
    index = 0
    
    if letter_list != []:
        print(textfile, "will be corrected now. To correct the shown text, put in the full, corrected text. To skip, type s. To end correction, type e. (Note: In that case, the file will still be saved normally).")
        # Initiate new text variable, onto which the new text will be saved
        output_txt = txt[0:letter_list[0]]
        # Iterate over found instances
        for item in letter_list:
            # Show the part to be corrected:
            # 1. Search when the index for the next line break is
            try:
                line_break = [m.start() for m in re.finditer("\n", txt[item:-1])][0]
            # In case there is no next line break, use the length of the text, yielding the last index
            except:
                line_break = len(txt) - item
            print(txt[item:item+line_break])
            # Input the correction
            correction = input("Correction:")
            if correction == "s":
                # Save the uncorrected text
                output_txt = output_txt + txt[item:item+line_break]
            elif correction == "e":
                # Save the uncorrected text and the rest of the text
                output_txt = output_txt + txt[item:-1] + txt[-1]
                break
            else:
                # Save the correction
                output_txt = output_txt + correction
            # Add 1 to the index
            index+=1
            # Check if the loop has one more iteration. If not, save the rest of the text
            if index == maxx:
                output_txt = output_txt + txt[item+line_break:-1]
                break
            # If yes, save only up until before the next iteration
            else:
                output_txt = output_txt + txt[item+line_break:letter_list[index]]
    else:
        output_txt = txt
    return output_txt

def save_file(txt, filename):
    # Script to save the text file
    filename = filename.split('\\')[1]
    filename = os.path.join("testtexte_verbessert", filename)
    #filename = os.path.join("18th_century_corr1", filename)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(txt)
    print(filename, "File saved!")
    return

def main():
    for textfile in glob.glob(os.path.join("testtexte", "*.*")):
    #for textfile in glob.glob(os.path.join("18th_century", "*.*")):
        with open(textfile, "r", encoding="utf-8") as f:
            txt = f.read().lower()
        #print(txt)
        txt = correct_s(txt)
        #print(txt)
        txt = single_characters(txt)
        #print(txt)
        txt = delete_specials(txt)
        #print(txt)
        txt = common_mistakes(txt)
        #print(txt)
        txt = correct_consonants(txt, textfile)
        #print(txt)
        save_file(txt, textfile)

main()


