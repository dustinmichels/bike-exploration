import multiprocessing
from pathlib import Path

import numpy as np
import pandas as pd
from rich import print
from tqdm import tqdm

from . import load

# from convert import (
#     FitParseException,
#     convert_fit_file,
#     extract_multiline,
#     process_activities_dataframe,
#     unzip_file,
# )


def load_activities(strava_dir: str):
    path = Path(strava_dir).joinpath("activities.csv")
    df = pd.read_csv(path)
    return load.process_activities_dataframe(df)


def unzip_activities(df):
    new_paths = []
    for f in tqdm(list(df["Filename"])):
        fp = Path(IN_DIR).joinpath(f)
        try:
            new_path = str(unzip_file(filepath=fp, out_dir=OUT_DIR))
        except FileNotFoundError as e:
            print("Error!", e)
            new_path = ""
        new_paths.append(new_path)
    df["new_path"] = new_paths

    # remove rows where new_filename is missing
    print("Removing {} rows with missing files".format(len(df[df["new_path"] == ""])))
    df = df[df["new_path"] != ""]

    return df


def process_file(filepath: str) -> str:
    """Inner function of convert_activities to be used with multiprocessing"""
    try:
        new_path = convert_fit_file(filepath=filepath)
    except FitParseException as e:
        new_path = ""
    return str(new_path)


def convert_activities(df):
    filepaths = list(df["new_path"])

    # Use imap_unordered for progress tracking with tqdm
    with multiprocessing.Pool() as pool:
        new_paths = list(tqdm(pool.imap(process_file, filepaths), total=len(filepaths)))

    df["new_path"] = new_paths

    # remove rows where new_filename is missing
    print(
        "Removing {} rows that could not be converted".format(
            len(df[df["new_path"] == ""])
        )
    )
    df = df[df["new_path"] != ""]

    return df


def extract_polylines(df):
    geo = []
    for f in tqdm(list(df["new_path"])):
        try:
            multiline = extract_multiline(filepath=f)
        except Exception as e:
            multiline = np.nan
        geo.append(multiline)
    df["multiline"] = geo

    # remove rows where multiline is missing
    print(
        "Removing {} rows with missing polylines".format(
            len(df[df["multiline"].isna()])
        )
    )
    df = df[~df["multiline"].isna()]

    return df


def main(df):
    df = load_activities()
    df = unzip_activities(df)

    # rename multiline column to "geometry"
    df.rename(columns={"multiline": "geometry"}, inplace=True)


if __name__ == "__main__":
    main()
