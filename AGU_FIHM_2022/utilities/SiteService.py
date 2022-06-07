import chunk
import requests
import pandas as pd
from io import StringIO
from time import sleep
import numpy as np

class SiteService:
    base_url: str = "https://waterservices.usgs.gov/nwis/site/"

    def get_raw_data(self, sites, session):
        # Set parameters
        params = {
            "format": "rdb",
            "sites": sites,
            "parameterCd": "00060",
            "siteOutput": "expanded",
            "siteStatus": "all"
            }

        # Get raw compressed data
        with session.get(self.base_url, params=params) as response:
            sleep(0.2)
            return response.text

    def get_dataframe(self, sites, session):
        # Get raw data
        raw_data = self.get_raw_data(sites, session)

        # Parse data
        try:
            df = pd.read_csv(StringIO(raw_data), comment="#", sep="\t")
        except pd.errors.EmptyDataError:
            return pd.DataFrame()

        # Drop first row
        df = df.iloc[1:,:]
        
        # Return no data
        if df.empty:
            return df

        # Return
        return df

    def get(self, sites, chunk_size=100):
        # Split up site list
        num_chunks = int(len(sites) // chunk_size) + 1
        chunks = np.array_split(sites, num_chunks)

        # Get raw compressed data
        with requests.Session() as session:
            # Retrieve chunks
            dfs = []
            for idx, c in enumerate(chunks):
                print(f"Retrieving chunk: {idx}")
                df = self.get_dataframe(",".join(c), session)
                dfs.append(df)

            # Compare to sites
            retrieved = pd.concat(dfs, ignore_index=True)
            mask = np.isin(sites, retrieved["site_no"])
            missing = sites[~mask]
            print(f"These sites were missing:")
            print(missing)

            # Retrieve chunks
            dfs = []
            for s in missing:
                print(f"Retrieving missing site: {s}")
                df = self.get_dataframe(s, session)
                dfs.append(df)

            # Combine sites
            dfs.append(retrieved)
            return pd.concat(dfs, ignore_index=True)
