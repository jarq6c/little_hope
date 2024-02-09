#!/usr/bin/env python3
# Import tools to retrieve data and detect events
from hydrotools.nwis_client.iv import IVDataService
from hydrotools.events.event_detection import decomposition as ev
import matplotlib.pyplot as plt

# Retrieve streamflow observations for Little Hope Creek
client = IVDataService(value_time_label="value_time")
observations = client.get(
    sites='02146470', 
    startDT='2019-10-01', 
    endDT='2020-09-30'
    )

# Drop extra columns to be more efficient
observations = observations[['value_time', 'value']]

# Check for duplicate time series, keep first by default
observations = observations.drop_duplicates(subset=['value_time'])

# Resample to hourly, keep first measurement in each 1-hour bin
observations = observations.set_index('value_time')
observations = observations.resample('H').first().ffill()

# Detect events
events = ev.list_events(
    observations['value'],
    halflife='6H', 
    window='7D',
    minimum_event_duration='6H',
    start_radius='7H'
)

# Compute peak discharge for each event
events['peak'] = events.apply(
    lambda e: observations['value'].loc[e.start:e.end].max(), 
    axis=1
    )

# Plot a histogram of peak discharge values
plt.hist(events['peak'], bins=20, density=True)
plt.xlim(0.0,2000.0)
plt.xlabel('Peak Discharge (cfs)')
plt.ylabel('Relative Frequency')
plt.tight_layout()
plt.show()

# Plot the hydrograph
observations.plot(logy=True, legend=False)
observations.loc[events['start'], 'value'].plot(
    ax=plt.gca(), style='o'
)
plt.xlabel('Datetime (UTC)')
plt.ylabel('Discharge (cfs)')
plt.legend(['Streamflow','Event Start'])
plt.tight_layout()
plt.show()
