#!/usr/bin/python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=no-value-for-parameter

import requests
import pandas as pd
import streamlit as st
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../../'))
LOCATIONS_INTERMEDIATE_DIR = os.path.join(ROOT_DIR, 'data/inputs/static/locations/intermediate')

################################################################################
##### Query wikidata for all ISO-3166-1 countries                         ######
################################################################################

# Wikidata query for ISO-3166-1 codes
# Use at https://query.wikidata.org/

# Workaround for a bug in generating urls for wikidata queries:
# Use the UI at https://query.wikidata.org/ to get the query url by entering these queries
# and then click the "Link" button -> SPARQL endpoint -> copy link address.
# This gives you the url for the query.

# SELECT DISTINCT ?country ?countryLabel ?capital ?capitalLabel
# WHERE
# {
#   ?country wdt:P31 wd:Q3624078 .
#   #not a former country
#   FILTER NOT EXISTS {?country wdt:P31 wd:Q3024240}
#   #and no an ancient civilisation (needed to exclude ancient Egypt)
#   FILTER NOT EXISTS {?country wdt:P31 wd:Q28171280}
#   OPTIONAL { ?country wdt:P36 ?capital } .
#
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
# }
# ORDER BY ?countryLabel

iso_3166_1_url = 'https://query.wikidata.org/sparql?query=%23added%20before%202016-10%0ASELECT%20DISTINCT%20%3Fcountry%20%3FcountryLabel%20%3FthreeLetterCode%20%3FnumericCode%20%3FtwoLetterCode%0AWHERE%0A%7B%0A%20%20%3Fcountry%20wdt%3AP298%20%3FthreeLetterCode.%0A%20%20%3Fcountry%20wdt%3AP299%20%3FnumericCode.%0A%20%20%3Fcountry%20wdt%3AP297%20%3FtwoLetterCode.%0A%20%20%23not%20a%20former%20country%0A%20%20FILTER%20NOT%20EXISTS%20%7B%3Fcountry%20wdt%3AP31%20wd%3AQ3024240%7D%0A%20%20%23and%20no%20an%20ancient%20civilisation%20(needed%20to%20exclude%20ancient%20Egypt)%0A%20%20FILTER%20NOT%20EXISTS%20%7B%3Fcountry%20wdt%3AP31%20wd%3AQ28171280%7D%0A%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22%20%7D%0A%7D%0AORDER%20BY%20%3FcountryLabel'  # pylint: disable=line-too-long
countries = requests.get(iso_3166_1_url, params={'format': 'json'}).json()['results']['bindings']
country_df = pd.json_normalize(countries)
country_df = country_df.rename(columns={
    'country.value': 'wikidata_id',
    'twoLetterCode.value': 'country_iso_3166-1_alpha-2',
    'numericCode.value': 'country_iso_3166-1_numeric',
    'threeLetterCode.value': 'region_code',
    'countryLabel.value': 'region_name'
})
country_df = country_df[['wikidata_id', 'country_iso_3166-1_alpha-2', 'country_iso_3166-1_numeric',
                         'region_code', 'region_name']]
country_df['wikidata_id'] = country_df['wikidata_id'].apply(lambda s: s.split('/')[-1])
country_df['region_code_type'] = 'iso_3166-1'
country_df['country_iso_3166-1_alpha-3'] = country_df['region_code']
country_df['region_code_level'] = 1
country_df['parent_region_code'] = 'WORLD'
country_df['subdivision_type'] = 'countries'
country_df['region_type'] = 'country'
country_df['leaf_region_code'] = country_df['region_code']
country_df['level_1_region_code'] = country_df['region_code']
country_df['level_2_region_code'] = None
country_df['level_3_region_code'] = None
st.subheader('Countries including duplicate ISO-3166-1 / ISO-3166-2 regions')
st.write(country_df)

################################################################################
##### Remove duplicates for regions that could appear as either Level 1   ######
##### or as Level 2 regions, based on whether data sources are separate   ######
################################################################################

# Treat Netherlands + Aruba + Curaçao + Sint Maarten (Dutch part) as a single level 1 entity
country_df = country_df[country_df['wikidata_id'] != 'Q55']

# These regions appear as both ISO-1 and ISO-2, but we will count them as ISO-2
# so we remove them from the ISO-1 list
# Leave as ISO1 because they have separate data sources: Taiwain, Hong Kong, Macao
regions_to_remove_from_iso1 = {
    'ALA': 'Åland Islands', # Finland: FI-01

    'BLM': 'Saint Barthélemy', # France: FR-BL Saint Barthélemy (BL)
    'GUF': 'French Guiana', # France: FR-GF French Guiana (GF)
    'GLP': 'Guadeloupe', # France: FR-GP Guadeloupe (GP)
    'MAF': 'Saint Martin (French part)', # France: FR-MF Saint Martin (MF)
    'MTQ': 'Martinique', # France: FR-MQ Martinique (MQ)
    'NCL': 'New Caledonia', # France: FR-NC New Caledonia (NC)
    'PYF': 'French Polynesia', # France: FR-PF French Polynesia (PF)
    'SPM': 'Saint Pierre and Miquelon', # France: FR-PM Saint Pierre and Miquelon (PM)
    'REU': 'Réunion', # France: FR-RE Réunion (RE)
    'ATF': 'French Southern and Antarctic Lands', # France: FR-TF French Southern Territories (TF)
    'WLF': 'Wallis and Futuna', # France: FR-WF Wallis and Futuna (WF)
    'MYT': 'Mayotte', # France: FR-YT Mayotte (YT)

    'SJM': 'Svalbard and Jan Mayen', # Norway: NO-21 Svalbard, NO-22 Jan Mayen

    'BES': 'Caribbean Netherlands', # Netherlands: NL-BQ1 Bonaire (BQ), NL-BQ2 Saba (BQ), NL-BQ3 Sint Eustatius (BQ)
    'ABW': 'Aruba', # Netherlands: NL-AW Aruba (AW)
    'CUW': 'Curaçao', # Netherlands: NL-CW Curaçao (CW)
    'SXM': 'Sint Maarten (Dutch part)', # Netherlands: NL-SX Sint Maarten (SX)

    'ASM': 'American Samoa', # United States: US-AS
    'GUM': 'Guam', # United States: US-GU
    'MNP': 'Northern Mariana Islands', # United States: US-MP
    'PRI': 'Puerto Rico', # United States: US-PR
    'UMI': 'United States Minor Outlying Islands', # United States: US-UM
    'VIR': 'United States Virgin Islands', # United States: US-VI
}

st.write(len(regions_to_remove_from_iso1))
country_df = country_df[~country_df['region_code'].isin(regions_to_remove_from_iso1.keys())]
st.subheader('Countries without duplicate ISO-3166-1 / ISO-3166-2 regions')

################################################################################
##### Generate datacommons ids using the known format for the dcids       ######
################################################################################

country_df['datacommons_id'] = country_df.apply(lambda x: 'country/' + x['region_code'], axis=1)

st.write(country_df)
st.write(country_df.shape)

country_df.to_csv(os.path.join(LOCATIONS_INTERMEDIATE_DIR, 'iso_3166_1_locations.csv'), index=False)
