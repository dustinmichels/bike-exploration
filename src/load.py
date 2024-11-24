"""Load and clean data"""

import pandas as pd


def process_activities_dataframe(df):
    # convert datetime
    df["Activity Date"] = pd.to_datetime(df["Activity Date"])
    # bike rides only
    df = df[df["Activity Type"].isin(["Ride", "E-Bike Ride"])].reset_index(drop=True)
    # select cols
    df = df[
        [
            "Activity ID",
            "Activity Date",
            "Activity Type",
            "Activity Name",
            "Elapsed Time",
            "Distance",
            "Filename",
        ]
    ]
    # remove rows where filename is missing
    df = df[~df["Filename"].isna()]
    return df
