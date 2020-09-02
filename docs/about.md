# Open COVID-19 Data
Google Research's Open COVID-19 Data project is an open source pipeline that aggregates public COVID-19 data sources into a single dataset. The data includes time series data for COVID-19 cases, deaths, tests, hospitalizations, discharges, intensive case unit (ICU) cases, ventilator cases, government interventions, and Google's Community Mobility Reports and Search Trends symptoms dataset.
## Table of Contents
- [About](#about)
- [Using the data](#using-the-data)
  - [Latest data](#latest-data)
  - [Attributions and Licenses](#attributions-and-licenses)
  - [Data Schema](#data-schema)
    - [Locations](#locations)
    - [Dates](#dates)
  - [For data owners](#for-data-owners)
- [Development](#development)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Pipeline Structure](#pipeline-structure)
  - [Adding a new data source](#adding-a-new-data-source)
- [Authors](#authors)
- [Data Sources](#data-sources)
  
    

## About
COVID-19 data is published from many distinct sources with highly heterogenous formats. The goal of this pipeline is to accept data in many different formats, and to process it into a standardized and consistent schema. Having data in a consistent schema allows researchers to build models quickly, while the pipeline is designed for engineers to add new data sources quickly.

The pipeline supports three ways of ingesting data:
- **Automatic downloads:** data that can be downloaded as a .csv or .xslx file from a consistent url
- **Manual downloads:** data that can be downloaded as a .csv or .xslx, but must be downloaded manually because the url changes
- **Scraped data:** data that is not machine-readable and must be scraped by a human (e.g. from charts, tables, pdfs, or occasionally tweets)

For each data source, this repository has a configuration file located in `src/config/sources` that specifies how the pipeline should map the original data into our schema. Raw data is fetched from the data source and written into a directory within `data/inputs`. Exported data that has been transformed into our schema is found in the `data/exports` directory.

## Using the data

### Latest data
If you just want to use the latest data for models, visualizations, or research, we provide aggregated data files under different licenses. This is to provide you with options so that you can use data with a license that is acceptable for your use case, while respecting the original licenses of the data sources.
- Aggregated data under a CC-BY license can be downloaded from [this link](https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/cc_by/aggregated_cc_by.csv)
- Aggregated data under a CC-BY-SA license can be downloaded from [this link](https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/cc_by_sa/aggregated_cc_by_sa.csv).
- Aggregated data under a CC-BY-NC license can be downloaded from [this link](https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/cc_by_nc/aggregated_cc_by_nc.csv).
- There are two data sources released under Google Terms of Service. To download or use the data, you must agree to the Google [Terms of Service](https://policies.google.com/terms).
  - Google's Community Mobility Reports can be downloaded from [this directory](data/exports/google_mobility_reports)
  - Google's Search Trends Symptoms Dataset can be downloaded from [this directory](data/exports/search_trends_symptoms_dataset)

### Attributions and Licenses
Please see the [Data Sources](#data-sources) section of this README to note the attributions and licenses for each source.

### Data Schema
#### Locations
Every location is assigned an `open_covid_region_code`, which is a unique hierarchical location code that can be used to join data across tables in this repository. The full list of locations that are assigned an `open_covid_region_code` can be found at `data/exports/locations/locations.csv`. Where available, we also provide a `datacommons_id` and `wikidata_id` field for each location.

Each `open_covid_region_code` has up to three levels:
- The first-level region codes are `ISO-3166-1` codes, e.g. `IT` for Italy
- The second-level region codes are, by default, `ISO-3166-2` codes. For example, `US-AL` for Alabama. However, in some locations, COVID-19 data is reported in administrative regions other than `ISO-3166-2`, so the choice of sub-country regions is informed partially by data availability.
- Third-level regions include cities and counties - within the United States counties are coded using `FIPS 6-4` codes.

#### Dates
All dates are mapped to `ISO 8601` format during data loading, e.g. `2020-08-15`.

### For Data Owners
We have carefully checked the license and attribution information on each data source included in this repository, and in many cases have contacted the data owners directly to ask how they would like to be attributed.

If you are the owner of a data source included here and would like us to remove data, add or alter an attribution, or add or alter license information, please do not hesitate to email us at open-covid-19-data@google.com and we will happily consider your request.

## Development
If you would like to run the pipeline locally or to contribute to the codebase, here are instructions for installation and adding new data sources.

### Installation
To install Python dependencies:
```bash
pip install pandas xlrd pyyaml python3-wget
```

### Usage
To run the main script that runs the entire pipeline on the data that is in `data/inputs`:
```bash
python src/scripts/export_data.py
```

In addition, there are two scripts that can be run to fetch new data and write it into `data/inputs`.

To fetch data that can be automatically downloaded:
```bash
python src/scripts/fetch_automatic_downloads.py
```
To fetch data from a spreadsheet in `data/inputs/scraped/spreadsheets/`:
```bash
python src/scripts/fetch_scraped_data.py
```

### Pipeline Structure
The pipeline is structured so that raw data is always fetched into `data/inputs` before being consumed by the rest of the pipeline. Data sources for each data type are then loaded into pandas dataframes with a standardized schema for dates, locations, and columns. These dataframes are joined into a single dataframe, which is then exported.
![pipeline](https://user-images.githubusercontent.com/1656622/82526711-7b9a7900-9ae9-11ea-85af-79597672b2e0.jpg)

### Adding a new data source<br>

Before adding a new data source, we go through an internal approval within Google to ensure compliance with licensing and terms. Once a data source is approved, you can add the data to the pipeline as follows:
##### 1. Register new data types in `src/config/data.yaml`:
* If the source includes a data type that isn't yet included in the data schema, register the data type in the schema by adding an entry to `src/config/data.yaml`.

##### 2. Add a new yaml file to `src/config/sources`.
* Specify the `fetch` parameters:<br>
  * `source_url`: where to download the data<br>
  * `method`: one of `AUTOMATIC_DOWNLOAD`, `MANUAL_DOWNLOAD`, `SCRAPED`, `STATIC`<br>
  * `file`: filename for the data source<br>
* Specify the `load` parameters.<br>
  * `function`: which function in `load_functions.py` to use to load the data. Most data sources can be loaded with `default_load_function`, but some data sources will have formatting that requires implementing a new function in `load_functions.py`.<br>
  * `read`: data sources are read using the `pandas.read_csv()` or `pandas.read_excel()` functions. The `read` field accepts key/val parameters that are passed to the appropriate pandas read function.
  * `dates`:<br>
    * `columns`: list of column names in the original data source that are required as arg to a function that will return the date in ISO-8601 format. This is often just a single column, but sometimes the year/month/date are in separate columns in the original data.<br>
    * `date_format`: the format of the date in the original data source
    * `parse_function`: most dates can be parsed using the `default` function in `date_utils.py`. If the data source has a date format that requires a parser that doesn't exist in `date_utils.py`, implement a separate function in that file.
  * `regions`:
    * `mapping_keys`: if a data source contains multiple regions but not ISO-3166 codes for the regions, the locations file at `data/exports/locations/locations.csv` must contain a column or list of columns that can be uniquely map the locations in the data to the `region_code` for that location. The `mapping_keys` field takes key/value fields where the key is the column in the locations file, and the value is the string name of the column in the original data source.
* Specify the `data` parameters:
  * These parameters follow the data schema specified in `src/config/data.yaml`, where the keys come from the data schema and the values are the column name in the original data source for the corresponding data.
* Specify the `attribution` parameters. These are used to generate the data source section of the README. The fields for existing data sources serve as an example of what to include.
* Specify the `license` parameters. These are used to generate the LICENSE file. The fields for existing data sources serve as an example of what to include.
* Specify the `cc_by` and `cc_by_sa` fields: we produce two aggregated csv files, one is licensed under `CC-BY` and the other is under `CC-BY-SA`. These fields specify whether the data can appear in each file.

##### 3. Update docs and licenses:
* When you run `src/scripts/export_data.py`, it will update the `README.md` as well as the `LICENSE` files within `data/exports`.

## Authors
This repository is created and maintained by Katie Everett, Dan Nanas, Maddy Myers (UCSD), Sumit Arora, and Ian Fischer.
