# About

This open source pipeline aggregates public COVID-19 data sources into a single dataset, which includes COVID-19 cases, deaths, tests, hospitalizations, discharges, intensive care unit (ICU) cases, ventilator cases, government interventions, and Google's COVID19 Community Mobility Reports. The aggregated data is designed for researchers to build models quickly, and the pipeline is designed for engineers to add new data sources quickly.

In particular, we support data that comes in three formats: data that can be downloaded automatically (generally a .csv or .xlsx from a stable url), data that can be downloaded manually (generally .csv or .xslx files without stable urls), and data that is not machine-readable and must be scraped by a human (from charts, tables, pdfs, or occasionally tweets).

## To use the data

##### Latest data
If you just want to use the latest data for models, visualizations, or research, we provide four aggregated data files under four different licenses. This is to provide you with options so that you can use data with a license that is acceptable for your use case, while respecting the original licenses of the data sources.
- The CC-BY aggregation can be downloaded from [this link](https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/cc_by/aggregated_cc_by.csv)
- The CC-BY-SA aggregation can be downloaded from [this link](https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/cc_by_sa/aggregated_cc_by_sa.csv).
- The CC-BY-NC aggregation can be downloaded from [this link](https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/cc_by_nc/aggregated_cc_by_nc.csv).
- The Google TOS data can be downloaded from [this link](https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/google_tos/aggregated_google_tos.csv). In order to download or use the data or reports, you must agree to the [Google Terms of Service](https://policies.google.com/terms).

##### Versioned data
Releases to the dataset are tagged so there is a stable Github url that points to each version of the data.

##### Attributions and Licenses
Please see the Data Sources section of this README to note the attributions and licenses for each source.

## For Data Owners
We have carefully checked the license and attribution information on each data source included in this repository, and in many cases have contacted the data owners directly to ask how they would like to be attributed.

If you are the owner of a data source included here and would like us to remove data, add or alter an attribution, or add or alter license information, please do not hesitate to email us at open-covid-19-data@google.com and we will happily consider your request.

# Technical Documentation

## Pipeline Structure
Data is fetched from the original source either as an automatic download, a manual download, or scraped by humans. All data goes into the `data/inputs` directory before being consumed by the rest of the pipeline. Data sources for each data type are then loaded into pandas dataframes with a standardized schema for dates, locations, and columns. These dataframes are joined into a single dataframe, which can then be exported.

![pipeline](https://user-images.githubusercontent.com/1656622/82526711-7b9a7900-9ae9-11ea-85af-79597672b2e0.jpg)

#### Locations
Locations are mapped to a standardized, hierarchical set of region codes. The full list of region codes can be found at `data/exports/locations/locations.csv`.

The first-level region codes are ISO-3166-1 codes. By default, the second-level region codes are ISO-3166-2 codes. However, in some locations, COVID-19 data is reported in administrative regions other than ISO-3166-2, so the choice of sub-country regions is informed partially by data availability. Third-level regions include cities and counties - within the United States counties are coded using FIPS 6-4 codes.

#### Dates
All dates are mapped to ISO 8601 format during data loading.

## Setup
To install Python dependencies:
```bash
pip install pandas xlrd pyyaml python3-wget
```

## To add a new data source:<br>

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
* When you run `src/scripts/export_data.py`, it will update the `README.md` as well as the `LICENSE` files within `data/exports`

# Authors
This repository is created and maintained by Katie Everett, Dan Nanas, Maddy Myers (UCSD), Sumit Arora, and Ian Fischer.


## Data Sources
#### Australia
**Source name:** covid19data.com.au ([link](https://www.covid19data.com.au/))<br>**Link to data:** https://www.covid19data.com.au/hospitalisations-icu<br>**Description:** Data is scraped manually from the charts provided at the source link. Data for Australia consists of time series data for current hospitalizations, ICU and ventilator cases.<br>**License:** Creative Commons Attribution 4.0 International ([link](https://creativecommons.org/licenses/by/4.0/))<br>**Last accessed:** 2020-08-25

#### COVIDTracking
**Source name:** COVID-19 Tracking Project ([link](https://github.com/COVID19Tracking/))<br>**Link to data:** https://github.com/COVID19Tracking/covid-tracking-data/tree/master/data<br>**Description:** Data is downloaded automatically from the source link. Data for the United States consists of time series data for current and cumulative hospitalizations.<br>**License:** Apache 2.0 ([link](https://github.com/COVID19Tracking/covid-tracking-data/blob/master/LICENSE))<br>**Last accessed:** 2020-08-27

#### Colombia
**Original data source:** GOV.CO ([link](https://www.datos.gov.co))<br>**Link to original data:** https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr/data<br>**Data aggregated by:** COVID-19 Colombia ([link](https://github.com/dfuribez/COVID-19-Colombia))<br>**License:** Creative Commons Attribution-ShareAlike 4.0 International ([link](https://creativecommons.org/licenses/by-sa/4.0/))<br>**Last accessed:** 2020-08-27

#### Czech Republic
**Source name:** National Health Information System, Regional Hygiene Stations, Ministry of Health of the Czech Republic ([link](https://onemocneni-aktualne.mzcr.cz/covid-19))<br>**Link to data:** https://onemocneni-aktualne.mzcr.cz/covid-19<br>**Description:** Data is scraped manually from the charts provided at the source link. Data for the Czech Republic consists of time series data for current ICU cases, and current and cumulative hospitalizations.<br>**Citation:**
```
Komenda M., Karolyi M., Bulhart V., Žofka J., Brauner T., Hak J., Jarkovský J., Mužík J., Blaha M., Kubát J., Klimeš D., Langhammer P., Daňková Š ., Májek O., Bartůňková M., Dušek L. COVID ‑ 19: Přehled aktuální situace v ČR. Onemocnění aktuálně [online]. Praha: Ministerstvo zdravotnictví ČR, 2020 [cit. 25.04.2020]. Dostupné z: https://onemocneni-aktualne.mzcr.cz/covid-19. Vývoj: společné pracoviště ÚZIS ČR a IBA LF MU. ISSN 2694-9423.
```
**Last accessed:** 2020-08-25

#### Denmark
**Source name:** Statens Serum Institute ([link](https://www.sst.dk/))<br>**Link to data:** https://www.sst.dk/da/corona/tal-og-overvaagning<br>**Description:** Data is manually scraped from charts at the source link. Data for Denmark consists of time series data for current hospitalizations and ICU cases.<br>**Last accessed:** 2020-08-25

#### Finland
**Source name:** Finnish institute for health and welfare ([link](https://thl.fi/en/web/thlfi-en))<br>**Link to data:** https://thl.fi/en/web/infectious-diseases/what-s-new/coronavirus-covid-19-latest-updates<br>**License:** Creative Commons Attribution 4.0 International ([link](https://creativecommons.org/licenses/by/4.0/))<br>**Last accessed:** 2020-08-25

#### France
**Source name:** data.gouv.fr ([link](https://www.data.gouv.fr/))<br>**Link to data:** https://www.data.gouv.fr/en/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/<br>**Description:** Data is scraped manually from the charts provided at the source link. Data for France consists of time series data for cumulative hospitalizations and ICU cases.<br>**License:** Open License 2.0 ([link](https://www.etalab.gouv.fr/licence-ouverte-open-licence))<br>**Last accessed:** 2020-08-27

#### Google's COVID19 Community Mobility Reports
**Source name:** https://www.google.com/covid19/mobility/<br>**Link to data:** https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv<br>**Help Center:** https://support.google.com/covid19-mobility<br>**Description:** These Community Mobility Reports aim to provide insights into what has changed in response to policies aimed at combating COVID-19. The reports chart movement trends over time by geography, across different categories of places.<br>**Terms:** In order to download or use the data or reports, you must agree to the Google [Terms of Service](https://policies.google.com/terms).<br>**License:** Google Terms of Service ([link](https://policies.google.com/terms))<br>**Citation:**
```
Google LLC "Google COVID-19 Community Mobility Reports".
https://www.google.com/covid19/mobility/ Accessed: <date>.
```
**Last accessed:** 2020-08-03

#### Iceland
**Source name:** Directorate of Health in Iceland (Embaetti landlaeknis) ([link](https://www.covid.is/data))<br>**Link to data:** https://www.covid.is/data<br>**Description:** Data is downloaded manually from the source link. Data for Iceland consists of time series data for current ICU cases, and current and cumulative hospitalizations.<br>**Last accessed:** 2020-06-22

#### Ireland
**Source name:** Health Protection Surveillance Centre ([link](https://www.hpsc.ie/))<br>**Link to data:** https://www.hpsc.ie/a-z/respiratory/coronavirus/novelcoronavirus/casesinireland/epidemiologyofcovid-19inireland/<br>**Description:** Data is scraped manually from daily situation reports. Data for Ireland consists of time series data for cumulative hospitalizations.<br>**License:** Creative Commons Attribution ShareAlike 3.0 ([link](https://creativecommons.org/licenses/by-sa/3.0/))<br>**Last accessed:** 2020-08-25

#### Italy
**Source name:** Dipartimento della Protezione Civile ([link](http://www.protezionecivile.gov.it/en/risk-activities/health-risk/emergencies/coronavirus))<br>**Link to data:** https://github.com/pcm-dpc/COVID-19<br>**Description:** Data is downloaded automatically from the source repository. Data for Italy consists of time series data for current hospitalizations, but we can also compute cumulative hospitalizations.<br>**License:** Creative Commons Attribution 4.0 International ([link](https://creativecommons.org/licenses/by/4.0/))<br>**Last accessed:** 2020-08-27

#### Japan
**Source name:** Toyo Keizai Online ([link](https://github.com/kaz-ogiwara/covid19))<br>**Link to data:** https://github.com/kaz-ogiwara/covid19<br>**Copyright notice:** Copyright (c) 2020 Kazuki OGIWARA / 荻原 和樹<br>**Description:** Data is downloaded automatically from the source repository. Data for Japan consists of time series data for current hospitalizations and ICU cases.<br>**License:** MIT ([link](https://github.com/kaz-ogiwara/covid19/blob/master/LICENSE))<br>**Last accessed:** 2020-08-03

#### Luxembourg
**Source name:** Luxembourg Ministry of Health ([link](https://data.public.lu/fr/datasets/donnees-covid19/#_))<br>**Link to data:** https://data.public.lu/fr/datasets/donnees-covid19/#_<br>**Description:** Data is downloaded automatically from the source link. Data for Luxembourg consists of time series data for current hospitalizations and ICU cases.<br>**License:** Creative Commons Zero 1.0 Universal ([link](https://creativecommons.org/share-your-work/public-domain/cc0/))<br>**Last accessed:** 2020-08-27

#### Moldova
**Source name:** Ministry of Health, Labour and Social Protection ([link](https://msmps.gov.md/))<br>**Link to data:** https://msmps.gov.md/ro/advanced-page-type/comunicate-de-presa<br>**Last accessed:** 2020-08-25

#### Netherlands
**Source name:** National Institute for Public Health and The Environment ([link](https://www.rivm.nl/coronavirus-covid-19/grafieken))<br>**Link to data:** https://www.rivm.nl/coronavirus-covid-19/grafieken<br>**Description:** Data is downloaded manually from the source link. Data for the Netherlands consists of time series data for current hospitalizations.<br>**Last accessed:** 2020-06-29

#### New Zealand
**Source name:** New Zealand Ministry of Health ([link](https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus))<br>**Link to data:** https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases<br>**Last accessed:** 2020-08-25

#### Norway
**Source name:** Norwegian Institute of Public Health ([link](www.fhi.no))<br>**Link to data:** https://www.fhi.no/en/id/infectious-diseases/coronavirus/daily-reports/daily-reports-COVID19/<br>**Last accessed:** 2020-06-22

#### Our World in Data
**Source name:** Our World in Data ([link](www.OurWorldInData.org))<br>**Link to data:** https://github.com/owid/covid-19-data/tree/master/public/data<br>**License:** Creative Commons Attribution 4.0 International ([link](https://creativecommons.org/licenses/by/4.0/))<br>**Citation:**
```
Data from Our World in Data has been collected, aggregated, and documented by Diana Beltekian, Daniel Gavrilov, Charlie Giattino, Joe Hasell, Bobbie Macdonald, Edouard Mathieu, Esteban Ortiz-Ospina, Hannah Ritchie, and Max Roser.
```
**Last accessed:** 2020-08-27

#### Oxford Covid-19 Government Response Tracker
**Source name:** Oxford Covid-19 Government Response Tracker ([link](https://github.com/OxCGRT/covid-policy-tracker))<br>**Link to data:** https://github.com/OxCGRT/covid-policy-tracker/blob/master/data/OxCGRT_latest.csv<br>**License:** Creative Commons Attribution 4.0 International ([link](https://creativecommons.org/licenses/by/4.0/))<br>**Citation:**
```
Thomas Hale, Sam Webster, Anna Petherick, Toby Phillips, and Beatriz Kira. (2020). Oxford COVID-19 Government Response Tracker. Blavatnik School of Government.
```
**Last accessed:** 2020-08-27

#### Philippines
**Source name:** Philippines Department of Health ([link](https://www.doh.gov.ph/))<br>**Link to data:** http://www.doh.gov.ph/covid19tracker<br>**Last accessed:** 2020-08-25

#### Spain
**Source name:** Ministerio de Sanidad, Consumo y Bienestar Social ([link](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm))<br>**Link to data:** https://cnecovid.isciii.es/covid19/resources/agregados.csv<br>**Description:** The data is downloaded automatically from the source link. Due to regional differences in hospitalization reporting, we do not aggregate across regions to produce country-level statistics for Spain.<br>**Last accessed:** 2020-08-27

#### Sweden
**Source name:** Public Health Agency of Sweden ([link](https://www.folkhalsomyndigheten.se/the-public-health-agency-of-sweden/))<br>**Link to data:** https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data<br>**Description:** Data is downloaded automatically from the source link. Data for Sweden consists of time series data for current ICU cases.<br>**Last accessed:** 2020-08-27

#### Switzerland
**Source name:** Switzerland Federal Office of Public Health BAG ([link](https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html))<br>**Link to data:** https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html<br>**Last accessed:** 2020-06-29

#### The New York Times
**Source name:** The New York Times COVID-19 Data ([link](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html))<br>**Link to data:** https://github.com/nytimes/covid-19-data<br>**License:** Creative Commons Attribution-NonCommercial 4.0 International ([link](https://creativecommons.org/licenses/by-nc/4.0/legalcode))<br>**Citation:**
```
Data from The New York Times, based on reports from state and local health agencies.
```
**Last accessed:** 2020-08-27

#### United Kingdom
**Source name:** GOV.UK ([link](https://www.gov.uk))<br>**Link to data:** https://www.gov.uk/government/publications/<br>**Description:** Data is downloaded manually from the publications provided at the source link. Data is aggregated across regions in England and reported at the country level for England, Scotland, Wales and Northern Ireland. Data consists of time series data for current hospitalizations.<br>**License:** Open Government License 3.0 ([link](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/))<br>**Last accessed:** 2020-06-23

