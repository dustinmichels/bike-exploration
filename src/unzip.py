import gzip
import shutil
from pathlib import Path

import fitparse
import gpxpy
import pandas as pd

type File = type[Path | str]


def unzip_file(filepath: File, out_dir: File) -> Path:
    """Unzip if file ends with .gz, otherwise just copy"""

    # if file is .gpx.gz... no it isn't
    if isinstance(filepath, str) and filepath.endswith(".gpx.gz"):
        filepath = filepath.replace(".gpx.gz", ".gpx")

    # if input is string, convert to pathlib.PosixPath
    if isinstance(filepath, str):
        filepath = Path(filepath)
    if isinstance(out_dir, str):
        out_dir = Path(out_dir)

    # validate inputs
    if not filepath.is_file():
        raise FileNotFoundError(f"File {filepath} does not exist")
    if not out_dir.is_dir():
        raise NotADirectoryError(f"Directory {out_dir} does not exist")

    # if file ends with .gz, unzip it
    if filepath.suffix == ".gz":
        out_filepath = out_dir.joinpath(filepath.name.replace(".gz", ""))
        with gzip.open(filepath, "rb") as f_in:
            with open(out_filepath, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        return out_filepath

    # otherwise, just copy the file
    else:
        out_filepath = out_dir.joinpath(filepath.name)
        shutil.copy2(filepath, out_filepath)
        return out_filepath
