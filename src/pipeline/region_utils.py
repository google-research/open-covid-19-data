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

import pandas as pd
import streamlit as st
import os

import config

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
LOCATIONS_PATH = os.path.join(ROOT_DIR, 'data/inputs/static/locations.csv')

def join_region_codes(data_df, params):
    reg_params = params['load']['regions']
    if 'single_region_code' in reg_params:
        data_df = join_single_region_code(data_df, reg_params['single_region_code'])
    else:
        data_df = join_on_keys(data_df, reg_params['mapping_file'], reg_params['mapping_keys'])
    return data_df

def join_single_region_code(data_df, single_region_code):
    data_df['region_code'] = single_region_code
    locations_df = pd.read_csv(LOCATIONS_PATH)
    locations_df = locations_df[config.all_region_columns()]
    data_df = data_df.merge(locations_df, on=['region_code'])
    return data_df

def join_on_keys(data_df, regions_path, mapping_keys):
    abs_path = os.path.abspath(os.path.join(os.path.join(__file__, '../../..'), regions_path))
    regions_df = pd.read_csv(abs_path)
    reversed_mapping_keys = {value:key for key, value in mapping_keys.items()}
    data_df = data_df.rename(columns=reversed_mapping_keys)
    data_df = data_df.merge(regions_df, on=list(mapping_keys.keys()), how='inner')
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
