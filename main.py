import multiprocessing
from pathlib import Path

import numpy as np
import pandas as pd
from rich import print
from tqdm import tqdm

from convert import (
    FitParseException,
    convert_fit_file,
    extract_track_polyline,
    process_activities_dataframe,
    unzip_file,
)

IN_DIR = "data/export"
OUT_DIR = "data/out"


def load_activities(path="data/strava/activities.csv"):
    df = pd.read_csv(path)
    return process_activities_dataframe(df)


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


# def convert_activities(df):
#     new_paths = []
#     for f in tqdm(list(df["new_path"])):
#         try:
#             new_path = convert_fit_file(filepath=f)
#         except FitParseException as e:
#             print("Error!", e)
#             new_path = np.nan

#         new_paths.append(str(new_path))
#     df["new_path"] = new_paths

#     # remove rows where new_filename is missing
#     print("Removing {} rows with missing files".format(len(df[df["new_path"].isna()])))
#     df = df[~df["new_path"].isna()]

#     return df


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


def get_polylines(df):
    polylines = []
    for f in tqdm(list(df["new_path"])):
        try:
            polyline = extract_track_polyline(filepath=f)
        except Exception as e:
            polyline = np.nan
        polylines.append(polyline)
    df["polyline"] = polylines

    # remove rows where polyline is missing
    print(
        "Removing {} rows with missing polylines".format(len(df[df["polyline"].isna()]))
    )
    df = df[~df["polyline"].isna()]

    return df


def main(df):
    df = load_activities()
    df = unzip_activities(df)


if __name__ == "__main__":
    main()
