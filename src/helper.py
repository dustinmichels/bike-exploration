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


# Example usage
# fit_to_gpx("example.fit", "output.gpx")
