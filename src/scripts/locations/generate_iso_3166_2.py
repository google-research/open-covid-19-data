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
import sys
import datacommons as dc

dc.set_api_key(os.environ['DATACOMMONS_API_KEY'])

PIPELINE_DIR = os.path.join(os.path.dirname(__file__), '../../', 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import path_utils


locations_df = pd.read_csv(os.path.join(path_utils.path_to('locations_input_dir'), 'iso_3166_2_locations_raw.csv'))
aggregations_df = pd.read_csv(os.path.join(path_utils.path_to('locations_input_dir'), 'iso_3166_2_aggregations.csv'))
country_df = pd.read_csv(os.path.join(path_utils.path_to('locations_intermediate_dir'), 'iso_3166_1_locations.csv'))


country_df = country_df[['country_iso_3166-1_alpha-2', 'country_iso_3166-1_alpha-3', 'country_iso_3166-1_numeric']]
st.subheader('Countries')
st.write(country_df)
aggregations_df = aggregations_df[['parent_region_code', 'child_region_code', 'region_code_level', 'subdivision_type']]

st.subheader('Locations')
st.write(locations_df)
st.subheader('Aggregations')
st.write(aggregations_df)

locations_df = locations_df.drop(columns=['region_code_level'])

level_2_df = aggregations_df[aggregations_df['region_code_level'] == 2]
level_2_df['country_iso_3166-1_alpha-2'] = level_2_df['parent_region_code']
level_2_df['level_2_region_code'] = level_2_df['child_region_code']
level_2_df['level_3_region_code'] = None

level_3_df = aggregations_df[aggregations_df['region_code_level'] == 3]
level_3_df['country_iso_3166-1_alpha-2'] = level_3_df.apply(lambda x: x['parent_region_code'].split('-')[0], axis=1)
level_3_df['level_2_region_code'] = level_3_df['parent_region_code']
level_3_df['level_3_region_code'] = level_3_df['child_region_code']

child_region_df = pd.concat([level_2_df, level_3_df])

locations_df = locations_df.merge(child_region_df, how='left', left_on=['region_code'], right_on=['child_region_code'])
locations_df['leaf_region_code'] = locations_df['region_code']

locations_df = locations_df.merge(country_df, how='left', on=['country_iso_3166-1_alpha-2'])
locations_df['level_1_region_code'] = locations_df['country_iso_3166-1_alpha-3']
locations_df = locations_df.drop(columns=['child_region_code'])
st.subheader('Merged')
st.write(locations_df)
st.write(locations_df.shape)


################################################################################
##### Get wikidata ids - query for all places with ISO-3166-2 codes       ######
################################################################################

# Wikidata query for ISO-3166-2 codes
# Use at https://query.wikidata.org/

# Workaround for a bug in generating urls for wikidata queries:
# Use the UI at https://query.wikidata.org/ to get the query url by entering these queries
# and then click the "Link" button -> SPARQL endpoint -> copy link address.
# This gives you the url for the query.

# SELECT ?code ?place ?placeLabel
# WHERE
# {
#   ?place wdt:P300 ?code.
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
# }
# ORDER BY ASC(?code)

st.subheader('Wikidata ids')
iso_3166_2_url = 'https://query.wikidata.org/sparql?query=SELECT%20%3Fcode%20%3Fplace%20%3FplaceLabel%0AWHERE%0A%7B%0A%20%20%3Fplace%20wdt%3AP300%20%3Fcode.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%0AORDER%20BY%20ASC(%3Fcode)'  # pylint: disable=line-too-long
wikidata_result = requests.get(iso_3166_2_url, params={'format': 'json'}).json()['results']['bindings']
wikidata_df = pd.json_normalize(wikidata_result)
wikidata_df = wikidata_df.rename(columns={
    'place.value': 'wikidata_id',
    'code.value': 'region_code',
    'placeLabel.value': 'wikidata_name',
})
wikidata_df['wikidata_id'] = wikidata_df['wikidata_id'].apply(lambda s: s.split('/')[-1])
wikidata_df = wikidata_df[['wikidata_id', 'region_code', 'wikidata_name']]
wiki_duplicates = wikidata_df[wikidata_df['region_code'].duplicated(keep=False)]
wiki_duplicates.to_csv(
    os.path.join(path_utils.path_to('locations_intermediate_dir'), 'wikidata_iso_3166_2_duplicates.csv'), index=False)
st.write('Wikidata original: ')
st.write(wikidata_df)
st.subheader('Wikidata duplicates: ')
st.write(wiki_duplicates)
st.write(wiki_duplicates.count())

wiki_ids_to_keep = pd.read_csv(os.path.join(path_utils.path_to('locations_input_dir'), 'wikidata_canonical_ids.csv'))
st.write(wiki_ids_to_keep)

wiki_duplicates_to_discard = wiki_duplicates[~wiki_duplicates['wikidata_id'].isin(wiki_ids_to_keep['wikidata_id'])]

wikidata_df = wikidata_df[~wikidata_df['wikidata_id'].isin(wiki_duplicates_to_discard['wikidata_id'])]

st.subheader('Wikidata deduped: ')
st.write(wikidata_df)

st.subheader('Remaining duplicates')
duplicates = wikidata_df[wikidata_df['region_code'].duplicated(keep=False)]
st.write(duplicates)
st.write(duplicates.count())

st.subheader('With wikidata ids')
locations_df = locations_df.merge(wikidata_df, how='left', on=['region_code'])
st.write(locations_df)
st.write(locations_df.count())

st.subheader('Duplicated region codes')
duplicated_region_codes = locations_df[locations_df['region_code'].duplicated(keep=False)]
st.write(duplicated_region_codes)


################################################################################
##### Query datacommons to get dcids                                       #####
################################################################################

query_str = '''
SELECT ?name ?dcid ?isoCode
WHERE {
  ?a typeOf Place .
  ?a name ?name .
  ?a isoCode ?isoCode .
  ?a dcid ?dcid
  }
'''
results = dc.query(query_str)

iso_level_2 = list(filter(lambda elem: elem['?dcid'].startswith('iso'), results))
iso_level_2_df = pd.DataFrame(iso_level_2)
iso_level_2_df = iso_level_2_df.rename(columns={
    '?name': 'datacommons_name',
    '?dcid': 'datacommons_id',
    '?isoCode': 'region_code'
})

# Filter out dcids that aren't ISO-3166-2 codes
# (These appear to be freebase ids from wikidata)
iso_level_2_df['real_iso'] = iso_level_2_df.apply(lambda x: '/m/' not in x['region_code'], axis=1)
iso_level_2_df = iso_level_2_df[iso_level_2_df['real_iso'] == 1]
iso_level_2_df = iso_level_2_df.drop(columns=['real_iso'])
#
st.subheader('Datacommons ids')
st.write(iso_level_2_df)
st.write(iso_level_2_df.shape)

st.subheader('Datacommons duplicates')
dc_duplicates = iso_level_2_df[iso_level_2_df['region_code'].duplicated(keep=False)]
st.write(dc_duplicates)

################################################################################
##### Join datacommons_ids                                                 #####
################################################################################

locations_df = locations_df.merge(iso_level_2_df, how='left', on=['region_code'])
st.write(locations_df)

locations_df.to_csv(
    os.path.join(path_utils.path_to('locations_intermediate_dir'), 'iso_3166_2_locations.csv'), index=False)
