# National Water Model Evaluation Demonstration
## Expanding the Scope of National Water Model Forecast Evaluations by using Open Source Python-based Workflows and Incorporating Social Vulnerability
### AGU Frontiers in Hydrology Meeting 2022 - Poster 120-023

*Jason A. Regina<sup>1</sup> & Arthur A. Raney<sup>2</sup>*

<sup>1</sup>Office of Water Prediction, NOAA/NWS, Tuscaloosa, AL, USA

<sup>2</sup>Consortium of Universities for the Advancement of Hydrologic Science, Inc., Cambridge, MA, USA (Formerly NOAA Pathways Intern, National Water Center)

#### Abstract
We explore the potential of the National Water Model (NWM) Medium Range Forecast (MRF) and Extended Analysis and Assimilation (EANA) to provide vulnerable communities with useful hydrological information with a focus on regions with sparse streamflow observations. The NWM generates a variety of streamflow forecasts and simulations for over 2.7 million stream reaches across the Conterminous United States (CONUS). The MRF is a 10-day streamflow forecast issued four times a day. The EANA is an observation driven streamflow simulation produced daily. We evaluate the performance of the MRF and EANA during two widespread flooding events with a focus on vulnerable communities as quantified by the Social Vulnerability Index (SVI). SVI is a quantitative metric of a community’s relative vulnerability to natural and human-caused disasters. We demonstrate how an NWM evaluation can include broader societal impacts using the SVI and use the EANA to supplement observations in forecast verification. We apply these methods using the OWPHydroTools suite of Python-based hydrological evaluation tools and the dask Python library for efficient parallel computations.

<sup><sub>AGU Frontiers in Hydrology Meeting, 19-24 June 2022 in San Juan, PR
Session 142579: Advancing the State-of-the-Science of Water Resources Modeling - Community Development at the Intersection of Domain, Data, and Computer Sciences</sup></sub>

### Viewing and Running the Demo

This demonstration can be viewed directly in GitHub by clicking on `demo.ipynb` above. If you would like to run this demonstration locally, you can use the instructions below. These instructions assume a Linux command-line environment with `git`, `make`, and knowledge of Jupyter Notebooks.

```console
# Clone the repository
git clone https://github.com/jarq6c/little_hope.git

# Change to AGU_2021 directory
cd AGU_FIHM_2022

# Create miniconda python environment
#  Note: This will retrieve and create a local miniconda environment
make

# Activate environment
source miniconda3/bin/activate

# Launch notebook demonstration
jupyter notebook demo.ipynb
```