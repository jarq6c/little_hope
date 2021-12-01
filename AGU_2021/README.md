# OWPHydroTools Demonstration
## Python-based Tools for Retrieving and Evaluating National Water Model Streamflow Simulations
### AGU Fall Meeting 2021 - Poster H450-1343

*Jason A. Regina<sup>1</sup> & Arthur A. Raney<sup>2</sup>*

<sup>1</sup>Office of Water Prediction, NOAA/NWS, Tuscaloosa, AL, USA

<sup>2</sup>Consortium of Universities for the Advancement of Hydrologic Science, Inc., Cambridge, MA, USA (Formerly NOAA Pathways Intern, National Water Center)

#### Abstract
The OWPHydroTools suite (https://github.com/NOAA-OWP/hydrotools) includes packages used to:
 - Asynchronously retrieve USGS streamflow observations as Pandas DataFrames
 - Efficiently retrieve National Water Model (NWM) streamflow simulations and forecasts from Google Cloud Platform as Pandas DataFrames
 - Generate evaluation metrics such as Nash-Sutcliffe Efficiency and Threat Score
 - Detect hydrological events in long streamflow time series and compute single-event metrics from hydrograph features

This set of python packages includes efficient algorithms suitable for use in enterprise evaluation of continental-scale hydrologic and hydraulic model outputs. We showcase the capability of these tools through an example evaluation at Little Hope Creek in Charlotte, North Carolina, USA. We demonstrate the utility of this tool set in an event-based evaluation of the NWM “open loop” simulation at Little Hope Creek that includes peak discharge error, volume error, timing errors, NNSE, and categorical statistics.

<sup><sub>Presented at the AGU Fall Meeting, 13-17, Dec., 2021, New Orleans, LA
Session H074 - Next generation water resources modeling: innovation at the intersection of domain, computer, and data sciences</sup></sub>
