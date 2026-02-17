"""
Demonstrate how to classify streamflow from a single site for display on a
USGS WaterWatch style map.
"""
from pathlib import Path
import json

import pandas as pd
import geopandas as gpd

def main():
    """
    This function loads and classifies streamflow observations using USGS
    day-of-year statistics and categories drawn from the WaterWatch maps.
    Required data is located in the same directory as this module.

    Required Files
    --------------
    usgs_08324000_streamflow.geojson: GeoJSON file
        This is a month of streamflow observations.
    usgs_08324000_stats.geojson: GeoJSON file
        These are the actual day-of-year statistics.
    
    Plan
    ----
    1. Load and process streamflow observations. This results in five values:
    the latest "real-time" observation and the mean streamflow aggregated for last
    complete 1-day, 7-days, 14-days, and 28-days of the available record.
    2. Load and process streamflow statistics. This step assumes the current day-of-year
    corresponds to the timestamp of the latest "real-time" observation.

    """
    # Load continuous streamflow, also called instantaneous values or "real time observations"
    #  GeoJSON returned by https://api.waterdata.usgs.gov/ogcapi/v0/collections/continuous
    streamflow = gpd.read_file("usgs_08324000_streamflow.geojson")[[
        "time",
        "value"
    ]]

    # Get data ready to resample to daily mean
    streamflow["time"] = pd.to_datetime(streamflow["time"])
    streamflow["value"] = streamflow["value"].astype(float)
    streamflow = streamflow.sort_values(
        by="time").drop_duplicates(
            subset="time").set_index("time")

    # Compute daily mean streamflow
    streamflow["samples"] = 1
    daily_streamflow = streamflow.resample("1D").agg({
        "value": "mean",
        "samples": "sum"
    })

    # Apply strict requirement for 96 real-time observations per day, this
    #   requirement can probably be relaxed in practice.
    #   This assumes 15-min continuous values
    #   This has the effect of dropping partial days from the record (i.e. the
    #   first and last days are dropped)
    daily_streamflow = daily_streamflow[daily_streamflow["samples"] == 96]

    # Extract values to classify
    #  NOTE Both the streamflow and daily_streamflow values are sorted, so
    #  we can use normal array indexing to get the last n-values
    site_values = pd.DataFrame({
        "water_watch_map": [
            "real_time", "1_day", "7_day", "14_day", "28_day", "high_day"
        ],
        "streamflow": [
            streamflow["value"].iloc[-1],
            daily_streamflow["value"].iloc[-1],
            daily_streamflow["value"].iloc[-7:].mean(),
            daily_streamflow["value"].iloc[-14:].mean(),
            daily_streamflow["value"].iloc[-28:].mean(),
            100.0 # Adding this fake value as a check
        ]
    })

    # Set the current day-of-year based on latest time in streamflow
    day_of_year = streamflow.index[-1].strftime("%m-%d")

    # Load and extract day-of-year statistics for a single site (USGS-08324000)
    #   GeoJSON returned by https://api.waterdata.usgs.gov/statistics
    with Path("usgs_08324000_stats.geojson").open("r", encoding="utf-8") as fi:
        data = json.loads(fi.read())["features"][0]["properties"]["data"][0]["values"]

    # Parse and extract thresholds for current day-of-year
    statistics = pd.DataFrame.from_records(data)
    statistics = statistics[statistics["time_of_year"] == day_of_year]

    # Determine bins to classify flow, this does not exactly match the WaterWatch
    #   categories which use some rounding and inconsistent logical operators.
    #   Assuming minimum flow is 0.0 (may not be a safe assumption)
    bins = [float(b) for b in statistics["values"].iloc[0]]
    percentiles = statistics["percentiles"].iloc[0]
    labels = [f"{percentiles[i-1]} to <{percentiles[i]}" for i in range(1, len(percentiles))]

    # Classify, left inclusive
    site_values["percentile_class"] = pd.cut(
        site_values["streamflow"],
        bins=bins,
        right=False,
        labels=labels
        ).astype(str)

    # Deal with edges
    site_values.loc[site_values["streamflow"] < min(bins), "percentile_class"] = "<5"
    site_values.loc[site_values["streamflow"] > max(bins), "percentile_class"] = ">95"

    # Add descriptive text
    descriptions = {
        "<5": "Low",
        "5 to <10": "Much below normal",
        "10 to <25": "Below normal",
        "25 to <50": "Normal",
        "50 to <75": "Normal",
        "75 to <90": "Above normal",
        "90 to <95": "Much above normal",
        ">95": "High"
    }
    site_values["description"] = site_values["percentile_class"].map(descriptions)

    print(site_values)
    print(bins)
    print(percentiles)

if __name__ == "__main__":
    main()
