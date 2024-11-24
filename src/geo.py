import gzip
import shutil
from pathlib import Path

import fitparse
import gpxpy
import pandas as pd

type File = type[Path | str]


def count_files(dir: File) -> int:
    if isinstance(dir, str):
        dir = Path(dir)
    return len(list(dir.glob("*")))


def extract_multiline(filepath: File) -> list[tuple[float, float]]:
    # Open the GPX file
    with open(filepath, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # List to store the polyline
    multiline = []

    # Iterate through tracks, segments, and points
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # Append latitude and longitude as a tuple (in geojson order)
                multiline.append((point.longitude, point.latitude))

    return multiline
