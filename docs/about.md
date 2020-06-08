## About

This open source pipeline aggregates public COVID-19 data sources, including COVID-19 hospitalization, ICU, and ventilator data for the countries listed in the Data Sources section. Adding other data types relevant to COVID-19 is welcome and supported.

The pipeline is designed for researchers to build models quickly and for engineers to add new data sources quickly. We support data sources that can be downloaded automatically in structured formats such as .csv and .xlsx, but also aggregate human-scraped data from charts, tables, pdfs, and (occasionally) tweets.

## To use the data
If you just want to use the data for models, visualizations, or research, you can download the aggregated csv directly from `data/exported/hospitalizations.csv`. Releases to the dataset are tagged so there is a stable Github url that points to each version of the data.

Please see the Data Sources section to note the attributions and licenses for each source. If you want to understand the data aggregation pipeline and how to contribute to the repository, read on.

## Pipeline Structure
Data is fetched from the original source either as an automatic download, a manual download, or scraped by humans. All data goes into the `data/inputs` directory before being consumed by the rest of the pipeline. Data sources for each data type are then loaded into pandas dataframes with a standardized schema for dates, locations, and columns. These dataframes are joined into a single dataframe, which can then be exported.

![pipeline](https://user-images.githubusercontent.com/1656622/82526711-7b9a7900-9ae9-11ea-85af-79597672b2e0.jpg)

#### Locations
Locations are mapped to a standardized, hierarchical set of region codes. The full list of region codes can be found at `data/inputs/static/locations.csv`.

The first-level region codes are ISO-3166-1 codes. By default, the second-level region codes are ISO-3166-2 codes. However, in some locations, COVID-19 data is reported in administrative regions other than ISO-3166-2, so the choice of sub-country regions is informed partially by data availability. Third-level regions include cities and counties.

#### Dates
All dates are mapped to ISO 8601 format during data loading.

## Setup
To install Python dependencies:
```bash
pip install pandas xlrd pyyaml python3-wget
```

## Repository Structure

### To add a new data source:<br>

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
    * `mapping_file`: if a data source contains multiple regions but not ISO-3166 codes for the regions, we use an auxiliary file to map the strings or codes in the source file, to the region codes used in this repository. These files exist already for many countries in `data/inputs/static/locations/regions`, or you can add a new file there.
    * `mapping_keys`: takes key/value fields where the key is the column in the mapping file, and the value is the string name of the column in the original data source.
* Specify the `data` parameters:
  * These parameters follow the data schema specified in `src/config/data.yaml`, where the keys come from the data schema and the values are the column name in the original data source for the corresponding data.
* Specify the `attribution` parameters. These are used to generate the data source section of the README. The fields for existing data sources serve as an example of what to include.
* Specify the `license` parameters. These are used to generate the LICENSE file. The fields for existing data sources serve as an example of what to include.
* Specify the `cc-by-sa` field: we produce two aggregated csv files, one is licensed under `CC-BY` and the other is under `CC-BY-SA`. This field determines whether this data can be included in the `CC-BY` file.
* Specify the `approved` field: set to `True` after the data source has been approved.

##### 3. Update docs and licenses:
* Run `src/scripts/generate_source_docs.py` to update `docs/sources_cc_by_sa.md` with the new data source.
* Run `src/scripts/generate_readme.py` to update the `README.md` at the root of the repo.
* Run `src/scripts/export_aggregated_licenses.py` to update the `LICENSE` files in `data/exports`.
