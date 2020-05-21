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

##### 2. Add the source to `src/config/sources.yaml`:
* Specify the `fetch` parameters:<br>
  * `source_url`: where to download the data<br>
  * `automatic_download`: True if the `source_url` is a stable endpoint<br>
  * `scraped`: True if requires human scraping of the data<br>

* Specify the `path` where the data lives in the `data` directory:<br>
  * `dir`: directory for this data source<br>
  * `file`: filename for the data source<br>
  * `find_recent`: True if the data requires updating, False for static/auxiliary files<br>

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
* Specify the `approved` field: set to True after the data source has been approved


##### 3. Add to `src/config/docs.yaml`:
* This file contains the source, attribution, and licensing information required to generate the data source section of the README, as well as the LICENSE file.
* The key in this yaml file should be the same as the key in `src/config/docs.yaml`, and the fields for the existing data sources serve as an example of what to include.

##### 4. Update docs and licenses:
* Run `src/scripts/generate_source_docs.py` to update `docs/sources.md` with the new data source.
* Run `src/scripts/generate_readme.py` to update the `README.md` at the root of the repo.
* Run `src/scripts/generate_license_file.py` to update the `LICENSE` file at the root of the repo.


## Data Sources
#### Australia
**Source name:** covid19data.com.au ([link](https://www.covid19data.com.au/))<br>**Link to data:** https://www.covid19data.com.au/hospitalisations-icu<br>**Description:** Data is scraped manually from the charts provided at the source link. Data for Australia consists of time series data for current hospitalizations, ICU and ventilator cases.<br>**License:** Creative Commons Attribution 4.0 International ([link](https://creativecommons.org/licenses/by/4.0/))<br>**Last accessed:** 2020-05-20

#### Austria
**Source name:** Federal Ministry of Social Affairs, Health, Care and Consumer Protection ([link](https://info.gesundheitsministerium.at/))<br>**Description:** Data is downloaded manually from the source link. Current hospitalizations and ICU cases for Austria are computed by multiplying the percent utilization by the number of beds available.<br>**License:** Creative Commons Attribution 4.0 International ([link](https://creativecommons.org/licenses/by/4.0/))<br>**Last accessed:** 2020-05-20

#### Colombia
**Original data source:** GOV.CO ([link](https://www.datos.gov.co))<br>**Link to original data:** https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr/data<br>**Data aggregated by:** COVID-19 Colombia ([link](https://github.com/dfuribez/COVID-19-Colombia))<br>**Description:** Data is automatically downloaded from the linked github repository, which is sourced from datos.gov.co. Data for Colombia consists of time series data for current hospitalizations and ICU cases.<br>**License:** Creative Commons Attribution-ShareAlike 4.0 International ([link](https://creativecommons.org/licenses/by-sa/4.0/))<br>**Last accessed:** 2020-05-20

#### Czech Republic
**Source name:** National Health Information System, Regional Hygiene Stations, Ministry of Health of the Czech Republic ([link](https://onemocneni-aktualne.mzcr.cz/covid-19))<br>**Link to data:** https://onemocneni-aktualne.mzcr.cz/covid-19<br>**Attribution:** Komenda M., Karolyi M., Bulhart V., Žofka J., Brauner T., Hak J., Jarkovský J., Mužík J., Blaha M., Kubát J., Klimeš D., Langhammer P., Daňková Š ., Májek O., Bartůňková M., Dušek L. COVID ‑ 19: Přehled aktuální situace v ČR. Onemocnění aktuálně [online]. Praha: Ministerstvo zdravotnictví ČR, 2020 [cit. 25.04.2020]. Dostupné z: https://onemocneni-aktualne.mzcr.cz/covid-19. Vývoj: společné pracoviště ÚZIS ČR a IBA LF MU. ISSN 2694-9423.<br>**Description:** Data is scraped manually from the charts provided at the source link. Data for the Czech Republic consists of time series data for current ICU cases, and current and cumulative hospitalizations.<br>**Last accessed:** 2020-05-20

#### Denmark
**Source name:** Statens Serum Institute ([link](https://www.sst.dk/))<br>**Link to data:** https://www.sst.dk/da/corona/tal-og-overvaagning<br>**Description:** Data is manually scraped from charts at the source link. Data for Denmark consists of time series data for current hospitalizations and ICU cases.<br>**Last accessed:** 2020-05-20

#### France
**Source name:** data.gouv.fr ([link](https://www.data.gouv.fr/))<br>**Link to data:** https://www.data.gouv.fr/en/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/<br>**Description:** Data is scraped manually from the charts provided at the source link. Data for France consists of time series data for cumulative hospitalizations and ICU cases.<br>**License:** Open License 2.0 ([link](https://www.etalab.gouv.fr/licence-ouverte-open-licence))<br>**Last accessed:** 2020-05-20

#### Iceland
**Source name:** Directorate of Health in Iceland (Embaetti landlaeknis) ([link](https://www.covid.is/data))<br>**Link to data:** https://www.covid.is/data<br>**Description:** Data is downloaded manually from the source link. Data for Iceland consists of time series data for current ICU cases, and current and cumulative hospitalizations.<br>**Last accessed:** 2020-05-20

#### Ireland
**Source name:** Health Protection Surveillance Centre ([link](https://www.hpsc.ie/))<br>**Link to data:** https://www.hpsc.ie/a-z/respiratory/coronavirus/novelcoronavirus/casesinireland/epidemiologyofcovid-19inireland/<br>**Description:** Data is scraped manually from daily situation reports. Data for Ireland consists of time series data for cumulative hospitalizations.<br>**License:** Creative Commons Attribution ShareAlike 3.0 ([link](https://creativecommons.org/licenses/by-sa/3.0/))<br>**Last accessed:** 2020-05-20

#### Italy
**Source name:** Dipartimento della Protezione Civile ([link](http://www.protezionecivile.gov.it/en/risk-activities/health-risk/emergencies/coronavirus))<br>**Link to data:** https://github.com/pcm-dpc/COVID-19<br>**Description:** Data is downloaded automatically from the source repository. Data for Italy consists of time series data for current hospitalizations, but we can also compute cumulative hospitalizations.<br>**License:** Creative Commons Attribution 4.0 International ([link](https://creativecommons.org/licenses/by/4.0/))<br>**Last accessed:** 2020-05-20

#### Japan
**Source name:** Toyo Keizai Online ([link](https://github.com/kaz-ogiwara/covid19))<br>**Link to data:** https://github.com/kaz-ogiwara/covid19<br>**Description:** Data is downloaded automatically from the source repository. Data for Japan consists of time series data for current hospitalizations and ICU cases.<br>**License:** MIT ([link](https://github.com/kaz-ogiwara/covid19/blob/master/LICENSE))<br>**Last accessed:** 2020-05-20

#### Luxembourg
**Source name:** Luxembourg Ministry of Health ([link](https://data.public.lu/fr/datasets/donnees-covid19/#_))<br>**Link to data:** https://data.public.lu/fr/datasets/donnees-covid19/#_<br>**Description:** Data is downloaded automatically from the source link. Data for Luxembourg consists of time series data for current hospitalizations and ICU cases.<br>**License:** Creative Commons Zero 1.0 Universal ([link](https://creativecommons.org/share-your-work/public-domain/cc0/))<br>**Last accessed:** 2020-05-20

#### Netherlands
**Source name:** National Institute for Public Health and The Environment ([link](https://www.rivm.nl/coronavirus-covid-19/grafieken))<br>**Link to data:** https://www.rivm.nl/coronavirus-covid-19/grafieken<br>**Description:** Data is downloaded manually from the source link. Data for the Netherlands consists of time series data for current hospitalizations.<br>**Last accessed:** 2020-05-20

#### Scotland
**Source name:** The Scottish Government ([link](https://www.gov.scot/))<br>**Link to data:** https://www.gov.scot/publications/trends-in-number-of-people-in-hospital-with-confirmed-or-suspected-covid-19/<br>**Description:** The data is downloaded manually from the source link. Data for Scotland consists of time series data for current hospitalizations and ICU cases.<br>**License:** Open Government License 3.0 ([link](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/))<br>**Last accessed:** 2020-05-20

#### Spain
**Source name:** Ministerio de Sanidad, Consumo y Bienestar Social ([link](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm))<br>**Link to data:** https://cnecovid.isciii.es/covid19/resources/agregados.csv<br>**Description:** The data is downloaded automatically from the source link. Due to regional differences in hospitalization reporting, we do not aggregate across regions to produce country-level statistics for Spain.<br>**Last accessed:** 2020-05-20

#### Sweden
**Source name:** Public Health Agency of Sweden ([link](https://www.folkhalsomyndigheten.se/the-public-health-agency-of-sweden/))<br>**Link to data:** https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data<br>**Description:** Data is downloaded automatically from the source link. Data for Sweden consists of time series data for current ICU cases.<br>**Last accessed:** 2020-05-20

#### Switzerland
**Source name:** Switzerland Federal Office of Public Health BAG ([link](https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html))<br>**Link to data:** https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html<br>**Last accessed:** 2020-05-20

#### United Kingdom
**Source name:** GOV.UK ([link](https://www.gov.uk))<br>**Link to data:** https://www.gov.uk/government/publications/<br>**Description:** Data is downloaded manually from the publications provided at the source link. Data is aggregated across regions in England and reported at the country level for England, Scotland & Wales. Data consists of time series data for current hospitalizations.<br>**License:** Open Government License 3.0 ([link](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/))<br>**Last accessed:** 2020-05-20

#### United States
**Source name:** COVID-19 Tracking Project ([link](https://github.com/COVID19Tracking/))<br>**Link to data:** https://github.com/COVID19Tracking/covid-tracking-data/tree/master/data<br>**Description:** Data is downloaded automatically from the source link. Data for the United States consists of time series data for current and cumulative hospitalizations.<br>**License:** Apache 2.0 ([link](https://github.com/COVID19Tracking/covid-tracking-data/blob/master/LICENSE))<br>**Last accessed:** 2020-05-20

