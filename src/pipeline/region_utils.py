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

# pylint: disable=unused-argument

import pandas as pd
import os

import config

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
LOCATIONS_PATH = os.path.join(ROOT_DIR, 'data/exports/locations/locations.csv')

def join_region_codes(data_df, params):
    reg_params = params['load']['regions']
    if 'single_region_code' in reg_params:
        data_df = join_single_region_code(data_df, reg_params['single_region_code'])
    else:
        data_df = join_on_keys(data_df, reg_params)
    return data_df

# This drops states (which have county = Unknown, state = state name, fips = NaN)
# It also drops New York City (which has county = New York City, state = New York, fips = NaN)
def join_nytimes_region_codes(data_df, params):
    locations_df = pd.read_csv(LOCATIONS_PATH)
    fips_data_df = data_df[data_df['fips'].notna()]
    fips_locations = locations_df[locations_df['region_code_type'] == 'fips_6-4']
    fips_data_df['padded_fips_code'] = fips_data_df['fips'].apply(lambda x: str(int(x)).zfill(5))
    fips_data_joined = fips_data_df.merge(fips_locations, left_on=['padded_fips_code'],
                                          right_on=['leaf_region_code'], how='left')
    return fips_data_joined

def join_mobility_region_codes(data_df, params):
    locations_df = pd.read_csv(LOCATIONS_PATH)
    iso1_data = data_df[
        data_df['country_region_code'].notna() &
        data_df['sub_region_1'].isna() &
        data_df['sub_region_2'].isna() &
        data_df['metro_area'].isna()]
    iso2_data = data_df[
        data_df['iso_3166_2_code'].notna() &
        data_df['census_fips_code'].isna() &
        data_df['metro_area'].isna()]
    fips_data = data_df[
        data_df['iso_3166_2_code'].isna() &
        data_df['census_fips_code'].notna() &
        data_df['metro_area'].isna()]
    iso1_locations = locations_df[locations_df['region_code_type'] == 'iso_3166-1']
    iso1_joined = iso1_data.merge(iso1_locations, left_on=['country_region_code'],
                                  right_on=['country_iso_3166-1_alpha-2'], how='left')
    iso2_locations = locations_df[locations_df['region_code_type'] == 'iso_3166-2']
    iso2_joined = iso2_data.merge(iso2_locations, left_on=['iso_3166_2_code'], right_on=['region_code'], how='left')
    fips_locations = locations_df[locations_df['region_code_type'] == 'fips_6-4']
    fips_data['padded_fips_code'] = fips_data['census_fips_code'].apply(lambda x: str(int(x)).zfill(5))
    fips_joined = fips_data.merge(fips_locations, left_on=['padded_fips_code'],
                                  right_on=['leaf_region_code'], how='left')
    joined_df = pd.concat([iso1_joined, iso2_joined, fips_joined])
    return joined_df

def join_single_region_code(data_df, single_region_code):
    data_df['region_code'] = single_region_code
    locations_df = pd.read_csv(LOCATIONS_PATH)
    locations_df = locations_df[config.all_region_columns()]
    data_df = data_df.merge(locations_df, on=['region_code'])
    return data_df

def join_on_keys(data_df, reg_params):
    mapping_keys = reg_params['mapping_keys']
    locations_df = pd.read_csv(LOCATIONS_PATH)
    if 'level_1_region_code' in reg_params:
        locations_df = locations_df[locations_df['level_1_region_code'] == reg_params['level_1_region_code']]
    reversed_mapping_keys = {value: key for key, value in mapping_keys.items()}
    data_df = data_df.rename(columns=reversed_mapping_keys)
    data_df = data_df.merge(locations_df, on=list(mapping_keys.keys()), how='inner')
    return data_df

def aggregate_and_append(data_df, params):
    reg_params = params['load']['regions']
    if 'aggregate_by' in reg_params:
        agg_by = reg_params['aggregate_by']
        columns_to_sum = config.col_params_to_col_list(params['data'])
        agg_dict = {columns_to_sum[i]: 'sum' for i in range(len(columns_to_sum))}
        agg_df = data_df.groupby(['date', agg_by]).agg(agg_dict).reset_index()
        agg_df = agg_df.rename(columns={agg_by: 'region_code'})
        data_df = data_df.append(agg_df, ignore_index=True)
        data_df = data_df.drop_duplicates(subset=['date', 'region_code'])
    return data_df
