from hydrotools.nwm_client.gcp import NWMDataService
from hydrotools.nwis_client.iv import IVDataService
from hydrotools.metrics import metrics
from hydrotools.svi_client import SVIClient
from utilities.SiteService import SiteService

import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from pathlib import Path
import geopandas as gpd

@dataclass
class WorkflowDefaults:
    store_path: str = "local_data.h5"

def get_sim(startDT, endDT, store_path):
    with pd.HDFStore(store_path) as store:
        # Set key
        key = "sim"

        # Retrieve data
        if key in store:
            df = store[key]
        else:
            # Start NWM Client
            client = NWMDataService()

            # Define function to get single simulation
            get_single_sim = lambda rt: client.get(
                    reference_time=rt,
                    configuration="analysis_assim_extend_no_da"
                )

            # Generate list of reference times
            times = pd.date_range(
                start=startDT,
                end=endDT,
                freq="1D"
            )+pd.Timedelta("16H")

            # Convert to strings
            rts = times.strftime("%Y%m%dT%HZ")

            # Retrieve data
            df = pd.concat([get_single_sim(rt) for rt in rts], ignore_index=True)

            # Save data
            store.put(
                value=df,
                key=key,
                format="table",
                complevel=1
            )

    # Clean-up simulations
    df = df[["usgs_site_code", "value_time", "value"]]
    df = df.drop_duplicates(["usgs_site_code", "value_time"], keep="first")
    df = df.groupby(["usgs_site_code", pd.Grouper(key="value_time", freq="1H")]).first()

    # Remove non-streamflow sites and convert to foot^3/s
    df = df.reset_index()
    df = df[df["usgs_site_code"].str.isdigit()]
    df.loc[:, "value"] = df["value"].div(0.3048 ** 3.0)
    return df

def get_site_data(sites, store_path):
    with pd.HDFStore(store_path) as store:
        # Set key
        key = "site_data"

        # Retrieve data
        if key in store:
            df = store[key]
        else:
            # Start client
            client = SiteService()

            # Retrieve data
            df = client.get(sites)

            # Save
            store.put(
                value=df,
                key=key,
                format="table",
                complevel=1
            )
    
    # Map state codes
    sc = pd.read_csv("USPS_state_codes.csv", dtype=str, comment="#").set_index("fips_cd")
    df["state_ab"] = df["state_cd"].map(sc["state_ab"])

    # Construct full fips
    df["fips"] = df["state_cd"].add(df["county_cd"])

    # Clean-up data
    return df[["site_no", "fips", "state_ab"]].set_index("site_no")

def get_obs(sites, startDT, endDT, store_path):
    with pd.HDFStore(store_path) as store:
        # Set key
        key = "obs"

        # Retrieve data
        if key in store:
            df = store[key]
        else:
            client = IVDataService()
            df = client.get(
                startDT=startDT,
                endDT=endDT,
                sites=sites
            )
            store.put(
                value=df,
                key=key,
                format="table",
                complevel=1
            )

    # Clean-up data
    df = df[["usgs_site_code", "value_time", "value"]]
    df = df.drop_duplicates(["usgs_site_code", "value_time"], keep="first")
    return df.groupby(["usgs_site_code", pd.Grouper(key="value_time", freq="1H")]).first()

def get_svi(stateCds, store_path):
    # Check store
    key = "svi"
    with pd.HDFStore(store_path) as store:
        # Retrieve data
        if key in store:
            all_data = store[key]
        else:
            # Retrieve data
            gdfs = []
            for s in stateCds:
                ofile = Path(f"gis/svi_data_{s}.geojson")
                print(ofile)
                if ofile.exists():
                    gdfs.append(gpd.read_file(ofile))
                else:
                    client = SVIClient()
                    gdf = client.get(
                        location=s,
                        geographic_scale="county",
                        year="2018",
                        geographic_context="national"
                        )

                    # Cannot store categories in GeoJSON format
                    cats = gdf.select_dtypes("category")
                    for col in cats:
                        gdf[col] = gdf[col].astype(str)
                    gdf.to_file(ofile, driver="GeoJSON")
                    gdfs.append(gdf)
            
            # Merge data data
            all_data = pd.concat(gdfs, ignore_index=True)
            all_data = pd.DataFrame(all_data.drop("geometry", axis=1))

            # Save
            store.put(
                value=all_data,
                key=key,
                format="table",
                complevel=1
            )

    # Clean-up
    all_data = all_data[all_data["theme"] == "svi"]
    return pd.DataFrame(all_data[["fips", "rank", "value"]]).set_index("fips")

def get_pairs(startDT, endDT, WORKFLOW_DEFAULTS):
    with pd.HDFStore(WORKFLOW_DEFAULTS.store_path) as store:
        # Set key
        key = "pairs"

        # Check store
        if key in store:
            return store[key]

        # Get simulations
        sim = get_sim(
            startDT=startDT,
            endDT=endDT,
            store_path=WORKFLOW_DEFAULTS.store_path
        )
        sites = sim["usgs_site_code"].astype(str).unique()

        # Get site information
        site_data = get_site_data(
            sites=sites,
            store_path=WORKFLOW_DEFAULTS.store_path
        )

        # Retrieve observations
        obs = get_obs(
            sites=sites,
            startDT=startDT,
            endDT=endDT,
            store_path=WORKFLOW_DEFAULTS.store_path
        )

        # Retrieve SVI data
        svi = get_svi(stateCds=site_data.dropna()["state_ab"].unique(), 
            store_path=WORKFLOW_DEFAULTS.store_path)

        # Pair data
        pairs = sim.set_index(["usgs_site_code", "value_time"])
        pairs = pairs.rename(columns={"value": "sim"})
        pairs["obs"] = obs["value"]
        pairs = pairs[pairs >= 0.0]
        pairs = pairs.dropna().reset_index()
        pairs["fips"] = pairs["usgs_site_code"].map(site_data["fips"])
        pairs["svi"] = pairs["fips"].map(svi["rank"])

        # Save
        store.put(
            value=pairs,
            key=key,
            format="table",
            complevel=1
        )
        
        return pairs

def main(WORKFLOW_DEFAULTS: WorkflowDefaults):
    # Evaluation parameters
    startDT = "2021-08-26"
    endDT = "2021-09-06"

    # Get pairs
    pairs = get_pairs(startDT, endDT, WORKFLOW_DEFAULTS)

    # Assess gage counts
    gages = pairs.drop_duplicates(["usgs_site_code"], keep="first")
    gages = gages[gages["svi"] >= 0.0]

    # Plot SVI of NWM Assimilation Gages
    plt.hist(gages["svi"], bins=21)
    plt.xlim(0.0, 1.0)
    plt.xlabel("National SVI Rank")
    plt.ylabel("Number of NWM Assimilation Gages")
    plt.tight_layout()
    plt.show()
    plt.close()

    # Get site information
    site_data = get_site_data(
        sites=pairs["usgs_site_code"],
        store_path=WORKFLOW_DEFAULTS.store_path
    )

    # Retrieve SVI data
    svi = get_svi(stateCds=site_data.dropna()["state_ab"].unique(), 
        store_path=WORKFLOW_DEFAULTS.store_path).reset_index()

    # Find ungaged counties
    mask = svi["fips"].isin(pairs["fips"])
    svi = svi[~mask]
    svi = svi[svi["rank"] >= 0.0]

    # Plot SVI of NWM Assimilation Gages
    plt.hist(svi["rank"], bins=21)
    plt.xlim(0.0, 1.0)
    plt.xlabel("National SVI Rank")
    plt.ylabel("Number of Counties w/o NWM Assimilation Gage")
    plt.tight_layout()
    plt.show()
    plt.close()

if __name__ == "__main__":
    WORKFLOW_DEFAULTS = WorkflowDefaults()
    main(WORKFLOW_DEFAULTS)
