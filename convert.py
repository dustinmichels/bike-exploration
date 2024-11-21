import gzip
import pathlib
import shutil

import fitparse
import gpxpy
import gpxpy.gpx

type File = type[pathlib.PosixPath | str]


def unzip_file(filepath: File, unzip_dir: File):
    """Unzip if file ends with .gz, otherwise just copy"""

    # Convert strings to pathlib.PosixPath
    if isinstance(filepath, str):
        # if filepath is .gpx.gz, not it isn't
        if filepath.endswith(".gpx.gz"):
            filepath = filepath.replace(".gpx.gz", ".gpx")
        filepath = pathlib.PosixPath(filepath)
    if isinstance(unzip_dir, str):
        unzip_dir = pathlib.PosixPath(unzip_dir)

    # verify good inputs
    if not filepath.is_file():
        raise FileNotFoundError(f"File {filepath} does not exist")
    if not unzip_dir.is_dir():
        raise NotADirectoryError(f"Directory {unzip_dir} does not exist")

    # if file ends with .gz, unzip it
    if filepath.suffix == ".gz":
        print("unzipping")
        unzipped_filepath = unzip_dir.joinpath(filepath.name.replace(".gz", ""))
        with gzip.open(filepath, "rb") as f_in:
            with open(unzipped_filepath, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        return unzipped_filepath
    else:
        print("copying")
        copied_filepath = unzip_dir.joinpath(filepath.name)
        shutil.copy2(filepath, copied_filepath)
        return filepath.name


def parse_file(path: pathlib.PosixPath, unzip_dir: str):

    # if file ends with .gz, unzip it
    if path.endswith(".gz"):
        with gzip.open(filepath, "rb") as f_in:
            with open(unzip_dir + "/" + filepath[:-3], "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)


def extract_track_polyline(gpx_file_path):
    # Open the GPX file
    with open(gpx_file_path, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # List to store the polyline
    polyline = []

    # Iterate through tracks, segments, and points
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # Append latitude and longitude as a tuple
                polyline.append((point.latitude, point.longitude))

    return polyline


def fit_to_gpx(fit_file_path, gpx_file_path):
    # Read the FIT file
    fitfile = fitparse.FitFile(fit_file_path)

    # Create a new GPX file
    gpx = gpxpy.gpx.GPX()

    # Add a track to the GPX
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Add a segment to the track
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Parse FIT records
    for record in fitfile.get_messages("record"):
        # Extract data
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

        # Add point to GPX if valid
        if latitude is not None and longitude is not None:
            gpx_segment.points.append(
                gpxpy.gpx.GPXTrackPoint(
                    latitude, longitude, elevation=elevation, time=time
                )
            )

    # Write GPX to a file
    with open(gpx_file_path, "w") as gpx_file:
        gpx_file.write(gpx.to_xml())


# Example usage
# fit_to_gpx("example.fit", "output.gpx")
