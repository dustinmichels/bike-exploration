import multiprocessing
from pathlib import Path

import numpy as np
import pandas as pd
from rich import print
from tqdm import tqdm

IN_DIR = "data/strava"
OUT_DIR = "data/out"

from src.process_files import load_activities, unzip_activities


def main():
    df = load_activities(IN_DIR)
    # df = unzip_activities(df)

    # rename multiline column to "geometry"
    # df.rename(columns={"multiline": "geometry"}, inplace=True)


if __name__ == "__main__":
    main()
