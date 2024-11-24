import gzip
import shutil
from pathlib import Path

import fitparse
import gpxpy
import pandas as pd

type File = type[Path | str]


class FitParseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def convert_fit_file(filepath: File) -> File:
    """
    Convert the fit file to a GPX file, delete the original, return the new filepath
    """

    # if input is string, convert to pathlib.PosixPath
    if isinstance(filepath, str):
        filepath = Path(filepath)

    # validate input
    if not filepath.is_file():
        raise FileNotFoundError(f"File {filepath} does not exist")

    # if file is not a .fit file, return same path
    if filepath.suffix != ".fit":
        return filepath

    # prepare out file
    out_file = filepath.with_suffix(".gpx")

    # convert the fit file to a gpx file
    try:
        _fit_to_gpx(filepath, out_file)
    except Exception as e:
        raise FitParseException(f"Error converting {filepath}: {e}")

    # delete the fit file
    filepath.unlink()

    # return the path to the GPX file
    return out_file


def _fit_to_gpx(fit_filepath: File, gpx_filepath: File):
    """Convert a FIT file to a GPX file"""

    # read the FIT file
    fitfile = fitparse.FitFile(str(fit_filepath))

    # create a new GPX file
    gpx = gpxpy.gpx.GPX()

    # add a track to the GPX
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # add a segment to the track
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # parse FIT records
    for record in fitfile.get_messages("record"):
        latitude = None
        longitude = None
        elevation = None
        time = None

        for record_data in record:
            if record_data.name == "position_lat":
                latitude = record_data.value * (180 / 2**31)  # Convert to degrees
            elif record_data.name == "position_long":
                longitude = record_data.value * (180 / 2**31)  # Convert to degrees
            elif record_data.name == "altitude":
                elevation = record_data.value
            elif record_data.name == "timestamp":
                time = record_data.value

        # add point to GPX if valid
        if latitude is not None and longitude is not None:
            gpx_segment.points.append(
                gpxpy.gpx.GPXTrackPoint(
                    latitude, longitude, elevation=elevation, time=time
                )
            )

    # write GPX to a file
    with open(gpx_filepath, "w") as gpx_file:
        gpx_file.write(gpx.to_xml())
