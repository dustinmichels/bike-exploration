import gzip
import json
import os
import pathlib

import pandas as pd
from rich import print


def unzip_activities(self):
    """
    Method to unzip .gz files to their native format (e.g. gpx, tcx, fit, etc.)
    Adapted from: https://github.com/dodo-saba/fit2gpx/blob/main/src/fit2gpx.py
    """

    # Step 0: Count number of unique activity ids (sometimes an activity has both .fit and .fit.gz in the folder)
    cnt_activites = len({f.split(".")[0] for f in os.listdir(self._dir_activities)})

    # Step 1: Find zip files
    zip_paths = [
        self._dir_activities + f for f in os.listdir(self._dir_activities) if ".gz" in f
    ]

    # 2. Unzip each file, and delete previous
    for path_zip in zip_paths:
        path_unzip = path_zip.replace(".gz", "")

        # Check if file has already been unzipped:
        if path_unzip in os.listdir(self._dir_activities):
            continue

        else:
            # Unzip file
            with gzip.open(path_zip, "rb") as f_in:
                with open(path_unzip, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Delete zip file
            os.remove(path_zip)

    # Step 3: Check the correct number of activities is given
    if self.status_msg:
        if len(os.listdir(self._dir_activities)) == cnt_activites:
            print(f"{len(zip_paths)} zipped files have been unzipped")
        else:
            print("ERROR: Certain files have been deleted. Oopsies.")
