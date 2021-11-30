# Import tools
from hydrotools.nwm_client import gcp as nwm
from hydrotools.nwis_client.iv import IVDataService
import pandas as pd
from functools import partial
from pathlib import Path

def retrieve_model_data():
    """Setup model data client and retrieve NWM simulations."""
    # Set up client
    client = nwm.NWMDataService()

    # Generate list of references times
    reference_dts = pd.date_range(
        start="2021-07-01 16:00",
        periods=31,
        freq="24H"
    )

    # Paramteters
    configuration="analysis_assim_extend_no_da"
    reference_times = [d.strftime("%Y%m%dT%-HZ") for d in reference_dts]

    # Cache model data
    print("Caching model data...")
    retrievals = []
    for rt in reference_times:
        # Retrieve single simulation
        print(f"Retrieving {rt}")
        try:
            sim = client.get(
                configuration=configuration,
                reference_time=rt
            )
        except ValueError as e:
            print(f"Unable to retrieve {rt}")
            print(e)
            continue

        # Append successful retrieval
        retrievals.append(
            partial(client.get,
                configuration=configuration, reference_time=rt)
        )
    print("Done")

    # Return cached dataframes
    return pd.concat([r() for r in retrievals], ignore_index=True)

def retrieve_observations(sim):
    """Get observations that overlap sim."""
    # Check for file
    if Path("obs.h5").exists():
        return pd.read_hdf("obs.h5")

    # Drop incompatible locations
    mask = sim["usgs_site_code"].str.contains(r"[a-zA-Z]")
    sim = sim[~mask]

    # Get matching observations
    client = IVDataService(value_time_label="value_time")

    # Retrieve observations
    df = client.get(
        sites=sim["usgs_site_code"].astype(str).unique(),
        startDT=sim["value_time"].min(),
        endDT=sim["value_time"].max()
    )

    # Save data
    df.to_hdf("obs.h5", key="data", format="table", complevel=1)
    return df

def main():
    # Get model data
    sim = retrieve_model_data()

    # Get observations
    obs = retrieve_observations(sim)

    print(obs)

if __name__ == "__main__":
    main()
