#!/usr/bin/env python3
# Import tools to retrieve data and detect events
from evaluation_tools.nwis_client.iv import IVDataService
from evaluation_tools.events.event_detection import decomposition as ev
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Retrieve streamflow observations for Little Hope Creek
observations = IVDataService.get(
    sites='02146470', 
    startDT='2019-10-01', 
    endDT='2020-09-30'
    )

# Drop extra columns to be more efficient
observations = observations[['value_date', 'value']]

# Check for duplicate time series, keep first by default
observations = observations.drop_duplicates(subset=['value_date'])

# Resample to hourly, keep first measurement in each 1-hour bin
observations = observations.set_index('value_date')
observations = observations.resample('H').first().ffill()

# Subset
start = pd.Timestamp("2020-03-03 06:00")
end = pd.Timestamp("2020-03-06 18:00")
observations = observations.loc[start:end, :]

# Estimate baseflow using straigh line method
observations['Baseflow'] = observations['value'].values
for i in range(1, observations['value'].count()):
    modeled = observations['Baseflow'].iloc[i-1] + 0.04
    observed = observations['value'].iloc[i]
    observations['Baseflow'].iloc[i] = min(modeled, observed)

# Rename
observations = observations.rename(columns={
    'value': 'Direct Runoff'
})

# Apply event criteria
event_flows = (observations['Direct Runoff'] > observations['Baseflow'])
events = ev.event_boundaries(event_flows)
events['start'] = events['start'] - pd.Timedelta('1H')

# Plot
ax = observations.plot(logy=True)
observations.loc[events.start, 'Baseflow'].plot(
    ax=ax,
    style='o',
    markersize=10,
    label='Event Start'
)
observations.loc[events.end, 'Baseflow'].plot(
    ax=ax,
    style='s',
    markersize=10,
    label='Event End'
)
ax.fill_between(
    observations.index, 
    observations['Baseflow'],
    observations['Direct Runoff']
    )
ax.fill_between(
    observations.index, 
    observations['Baseflow']
    )
plt.xlabel("Time (UTC)")
plt.ylabel("Discharge (cfs)")
plt.ylim(1.0,200.0)
plt.title("Baseflow Separation Using the Straight-line Method")
ax.legend()
plt.tight_layout()
plt.savefig('images/baseflow.png')
