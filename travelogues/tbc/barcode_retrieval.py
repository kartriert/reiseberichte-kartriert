"""This script helps to retrieve all the barcodes of the files that should be included in the output results.
In this script, an absolute path to the metadata directory on my PC is given as the files would only pollute this
repository.
"""
import errno
import glob
import os
from pathlib import Path

"""Path of the directory in which I stored the metadata files from the Travelogues corpus.
This depends on where the Travelogue files are stored. I normally don't want to re-upload everything on GitHub, so I
excluded the corpus from this repository.
"""
DATA_PATH: str = "/Users/sarahreb/Downloads/metadata-18/"
BARCODE_PATH: str = "../data/barcodes/"


def get_barcodes(century: str, path: str = DATA_PATH) -> None:
    """Function for retrieving the barcodes from the given directory.
    Stores the results in a TXT file.

    @param century: Define century (as string) of the files (17th, 18th or 19th)
    @param path: String containing the path to the directory of all needed files.
    """

    if not os.path.exists(os.path.dirname(BARCODE_PATH)):
        try:
            os.makedirs(os.path.dirname(BARCODE_PATH))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(BARCODE_PATH + "barcodes_%s.txt" % century, "w") as f:
        for file in glob.glob(path + "*.json"):
            barcode = Path(file).stem
            f.write('{}\n'.format(barcode))


get_barcodes('18')
