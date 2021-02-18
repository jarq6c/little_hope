# Little Hope Creek :: Peak Flow Analysis

This workflow demonstrates an application of event detection to generate a distribution of peak discharges from [Little Hope Creek](https://waterdata.usgs.gov/nc/nwis/inventory/?site_no=02146470&agency_cd=USGS) in North Carolina.

## Requirements

This workflow requires python 3.8, make, and assumes a Linux environment.

## Build and execute

The included `Makefile` will build the python environment and run the `little_hope.py` script. This script retrieves one year of streamflow data for Little Hope Creak and caches it in a local sqlite database. The script cleans and resamples the data before applying event detection. This workflow applies event detection using time series decomposition as found in the [Evaluation Tools](https://github.com/NOAA-OWP/evaluation_tools) package. For each event, the script computes peak discharge. The final output are two PNG files: a histogram of peak discharges and a streamflow hydrograph depicting the start times of all events.

To execute the workflow:

```console
# Clone this repository ...
$ git clone https://github.com/jarq6c/little_hope.git
$ cd little_hope

# ... or download this repository
$ wget https://github.com/jarq6c/little_hope/archive/main.zip
$ unzip main.zip
$ cd little_hope-main

# Run make to execute the entire workflow
$ make

# Alternatively, you can run the workflow from an annotated Jupyter Notebook
$ make notebook

# To clean-up and start over
$ make clean
```

## Source Code

```python
# little_hope.py

# Import tools to retrieve data and detect events
from evaluation_tools.nwis_client.iv import IVDataService
from evaluation_tools.events.event_detection import decomposition as ev
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

# Detect events
events = ev.list_events(
    observations['value'],
    halflife='6H', 
    window='7D',
    minimum_event_duration='6H',
    start_radius='6H'
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
plt.savefig('peak_histogram.png')
plt.close()

# Plot the hydrograph
observations.plot(logy=True, legend=False)
observations.loc[events['start'], 'value'].plot(
    ax=plt.gca(), style='o'
)
plt.xlabel('Datetime (UTC)')
plt.ylabel('Discharge (cfs)')
plt.legend(['Streamflow','Event Start'])
plt.tight_layout()
plt.savefig('streamflow.png')
```
