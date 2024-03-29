from cProfile import label
from hydrotools.nwm_client.gcp import NWMDataService
from hydrotools.nwis_client.iv import IVDataService
from hydrotools.metrics import metrics
from hydrotools.svi_client import SVIClient
from utilities.SiteService import SiteService
from utilities.AnnualPeakService import AnnualPeakService

import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from pathlib import Path
import geopandas as gpd
import dask.dataframe as dd
from dask.distributed import Client

plt.style.use('tableau-colorblind10')

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

def get_annual_peaks(sites, store_path):
    with pd.HDFStore(store_path) as store:
        # Set key
        key = "annual_peaks"

        # Retrieve data
        if key in store:
            df = store[key]
        else:
            # Start client
            client = AnnualPeakService()

            # Retrieve data
            df = client.get(sites)

            # Save
            store.put(
                value=df,
                key=key,
                format="table",
                complevel=1
            )

    # Clean-up data
    df.loc[:, "peak_va"] = df["peak_va"].apply(float)
    df.loc[:, "peak_dt"] = pd.to_datetime(df["peak_dt"], errors="coerce")
    return df[["site_no", "peak_dt", "peak_va"]].dropna()

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

def make_hist(arr, xlabel, ylabel, ofile):
    # Set font size
    plt.rc('font', size=8)

    # Get figure and axes
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)

    # Plot histogram
    ax.hist(arr, bins=21, edgecolor="black")
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()

    # Save
    plt.savefig(ofile)

    # Close
    plt.close(fig)

def make_xy(x, y, xlabel, ylabel, ofile):
    # Set font size
    plt.rc('font', size=8)

    # Get figure and axes
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)

    # Plot x vs. y
    ax.plot(x, y, "o")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()

    # Save
    plt.savefig(ofile)

    # Close
    plt.close(fig)

def evaluate(startDT, endDT, WORKFLOW_DEFAULTS):
    with pd.HDFStore(WORKFLOW_DEFAULTS.store_path) as store:
        # Set key
        key = "evaluation"

        # Check store
        if key in store:
            return store[key]

        # Get pairs
        pairs = get_pairs(startDT, endDT, WORKFLOW_DEFAULTS)

        # Assess gage counts
        gages = pairs.drop_duplicates(["usgs_site_code"], keep="first")
        gages = gages[gages["svi"] >= 0.0]

        # Plot SVI of NWM Assimilation Gages
        make_hist(
            arr=gages["svi"],
            xlabel="National SVI Rank",
            ylabel="Number of NWM Assimilation Gages",
            ofile="plots/svi_nwm_gages.png"
        )

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

        # Plot counties with no NWM gages
        make_hist(
            arr=svi["rank"],
            xlabel="National SVI Rank",
            ylabel="Number of Counties w/o NWM Assimilation Gage",
            ofile="plots/svi_nwm_counties.png"
        )

        # Use the 33.3th percentile of annual peak as a threshold for a categorical evaluation
        annual_peaks = get_annual_peaks(pairs["usgs_site_code"].astype(str).unique(), WORKFLOW_DEFAULTS.store_path)
        thresholds = annual_peaks.groupby("site_no").quantile(0.333)

        # Map thresholds
        pairs["threshold"] = pairs["usgs_site_code"].map(thresholds["peak_va"])

        # Apply thresholds
        pairs["obs_flood"] = (pairs["obs"] >= pairs["threshold"])
        pairs["sim_flood"] = (pairs["sim"] >= pairs["threshold"])

        # Convert categories to string
        pairs.loc[:, "usgs_site_code"] = pairs["usgs_site_code"].astype(str)

        # Setup default dask client
        dask_client = Client(n_workers=4, threads_per_worker=1)

        # Compute contingency tables
        meta = {
            "true_positive": "int64",
            "false_positive": "int64",
            "false_negative": "int64",
            "true_negative": "int64"
        }
        dask_pairs = dd.from_pandas(pairs[["usgs_site_code", "obs_flood", "sim_flood"]], npartitions=4).persist()
        ct = dask_pairs.groupby("usgs_site_code").apply(lambda c: metrics.compute_contingency_table(c.obs_flood, c.sim_flood), 
            meta=meta).compute()

        # Compute some basic metrics
        ct["POD"] = ct.apply(metrics.probability_of_detection, axis=1)
        ct["POFA"] = ct.apply(metrics.probability_of_false_alarm, axis=1)
        ct["TS"] = ct.apply(metrics.threat_score, axis=1)

        # Save
        store.put(
            value=ct,
            key=key,
            format="table",
            complevel=1
        )

        return ct

def main(WORKFLOW_DEFAULTS: WorkflowDefaults):
    # Evaluation parameters
    startDT = "2021-08-26"
    endDT = "2021-09-06"

    # Get evaluation results
    ct = evaluate(startDT, endDT, WORKFLOW_DEFAULTS)

    # Get pairs
    pairs = get_pairs(startDT, endDT, WORKFLOW_DEFAULTS)

    # Map svi to evaluation results
    svi = pairs.drop_duplicates(["usgs_site_code"], keep="first").set_index("usgs_site_code")
    ct["svi"] = svi["svi"]
    ct["fips"] = svi["fips"]

    # Plot evaluation results vs svi
    ct = ct.dropna()
    ct = ct.groupby("fips").mean()
    make_xy(ct["svi"], ct["TS"], 
        "National Ranked SVI",
        "Critical Success Index by US County",
        "plots/eval_results_sim.png"
        )

if __name__ == "__main__":
    WORKFLOW_DEFAULTS = WorkflowDefaults()
    main(WORKFLOW_DEFAULTS)
