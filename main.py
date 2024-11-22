from pathlib import Path

import numpy as np
import pandas as pd
from fitparse.base import FitHeaderError
from rich import print
from tqdm import tqdm

from convert import (
    convert_fit_file,
    extract_track_polyline,
    prepare_activities,
    unzip_file,
)

IN_DIR = "data/export"
OUT_DIR = "data/out"


def load_activities(path="data/strava/activities.csv"):
    df = pd.read_csv(path)
    return prepare_activities(df)


def unzip_activities(df):
    new_paths = []
    for f in tqdm(list(df["Filename"])):
        fp = Path(IN_DIR).joinpath(f)
        try:
            new_path = unzip_file(filepath=fp, out_dir=OUT_DIR)
        except FileNotFoundError:
            new_path = np.nan

        new_paths.append(new_path)
    df["new_path"] = new_paths

    # remove rows where new_filename is missing
    print("Removing {} rows with missing files".format(len(df[df["new_path"].isna()])))
    df = df[~df["new_path"].isna()]

    return df


def convert_activities(df):
    new_paths = []
    for f in tqdm(list(df["new_path"])):
        try:
            new_path = convert_fit_file(filepath=f)
        except FitHeaderError:
            new_path = np.nan

        new_paths.append(new_path)
    df["new_path"] = new_paths

    # remove rows where new_filename is missing
    print("Removing {} rows with missing files".format(len(df[df["new_path"].isna()])))
    df = df[~df["new_path"].isna()]

    return df


def main(df):
    df = load_activities()
    df = unzip_activities(df)


if __name__ == "__main__":
    main()
