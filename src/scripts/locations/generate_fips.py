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

import streamlit as st
import pandas as pd
import os
import sys
import datacommons as dc

dc.set_api_key(os.environ['DATACOMMONS_API_KEY'])

PIPELINE_DIR = os.path.join(os.path.dirname(__file__), '../../', 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import path_utils


df = pd.read_csv(os.path.join(path_utils.path_to('locations_input_dir'), 'us_state_and_county_fips_codes.csv'))
state_codes = pd.read_csv(os.path.join(path_utils.path_to('locations_input_dir'), 'us_states_and_numeric_codes.csv'))

################################################################################
##### Create table of fips codes with correct region_code formats          #####
################################################################################

st.write(state_codes)
merged = df.merge(state_codes, how='left', left_on=['state_code_fips'], right_on=['numeric_code'])
st.write(merged)

merged['parent_region_code'] = merged['alpha_code'].apply(lambda x: 'US-' + str(x))
st.write(merged)

merged['padded_state_fips'] = merged['state_code_fips'].apply(lambda x: str(x).zfill(2))
merged['padded_county_fips'] = merged['county_code_fips'].apply(lambda x: str(x).zfill(3))

merged['child_region_code'] = merged.apply(lambda x: x['padded_state_fips'] + x['padded_county_fips'], axis=1)

aggregations = merged[['parent_region_code', 'child_region_code']]
aggregations['subdivision_type'] = 'counties'
aggregations['region_type'] = 'county'
aggregations['child_region_code_type'] = 'fips_6-4'
st.write(aggregations)

locations = merged
st.subheader('locations')
locations['region_code'] = locations.apply(lambda x: x['parent_region_code'] + '-' + x['child_region_code'], axis=1)
locations['region_code_level'] = 3
locations['region_type'] = 'county'
locations['region_code_type'] = 'fips_6-4'
locations['leaf_region_code'] = locations['child_region_code']
locations = locations.astype({'leaf_region_code': str})
locations['country_iso_3166-1_alpha-2'] = 'US'
locations['country_iso_3166-1_alpha-3'] = 'USA'
locations['country_iso_3166-1_numeric'] = 840
locations['level_1_region_code'] = 'USA'
locations['level_2_region_code'] = locations['parent_region_code']
locations['level_3_region_code'] = locations['region_code']
st.write(locations)
st.write(locations.shape)

################################################################################
##### Query datacommons to get dcids                                       #####
################################################################################

datacommons_query_str = '''
SELECT ?name ?dcid ?geoId ?wikidataId
WHERE {
  ?a typeOf County .
  ?a name ?name .
  ?a geoId ?geoId .
  ?a wikidataId ?wikidataId .
  ?a dcid ?dcid
  }
'''
dc_results = dc.query(datacommons_query_str)
dc_df = pd.DataFrame(dc_results)
dc_df = dc_df.rename(columns={
    '?name': 'datacommons_name',
    '?dcid': 'datacommons_id',
    '?wikidataId': 'wikidata_id',
    '?geoId': 'fips_code'
})

dc_df = dc_df.drop_duplicates()

# New York County has two wikidata ids in datacommons:
# Q500416 (correct)
# Q11299 (incorrect - this is Manhattan not the fips county)
dc_df = dc_df[dc_df['wikidata_id'] != 'Q11299']
st.subheader('dc duplicate: ')
duplicate = dc_df[dc_df.duplicated(subset=['fips_code'])]
st.write(duplicate)

# There are four FIPS codes that don't get returned in the datacommons query
# because they don't have wikidata ids in datacommons:
# 46102 -> Q495201
# 02158 -> Q379474
# 02195 -> Q25408755
# 02198 -> Q18120072
add_to_dc_result = [
    {
        'datacommons_name': 'Oglala Lakota County',
        'datacommons_id': 'geoId/46102',
        'wikidata_id': 'Q495201',
        'fips_code': '46102'
    },
    {
        'datacommons_name': 'Kusilvak Census Area',
        'datacommons_id': 'geoId/02158',
        'wikidata_id': 'Q379474',
        'fips_code': '02158'
    },
    {
        'datacommons_name': 'Petersburg Borough',
        'datacommons_id': 'geoId/02195',
        'wikidata_id': 'Q25408755',
        'fips_code': '02195'
    },
    {
        'datacommons_name': 'Prince of Wales-Hyder Census Area',
        'datacommons_id': 'geoId/02198',
        'wikidata_id': 'Q18120072',
        'fips_code': '02198'
    }
]
add_to_dc_df = pd.DataFrame(add_to_dc_result)
dc_df = pd.concat([dc_df, add_to_dc_df])

# Join datacommons codes
locations = locations.merge(dc_df, how='outer', left_on='leaf_region_code', right_on='fips_code')

st.write(locations)
st.write(locations.shape)

locations = locations.drop(columns=[
    'state_code_fips',
    'county_code_fips',
    'state_name',
    'alpha_code',
    'numeric_code',
    'padded_state_fips',
    'padded_county_fips',
    'child_region_code',
    'fips_code'])

st.write(locations.columns)

locations.to_csv(os.path.join(path_utils.path_to('locations_export_dir'), 'fips_locations.csv'), index=False)
