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
import os

import load_data
import config

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
LOCATIONS_PATH = os.path.join(ROOT_DIR, 'data/exports/locations/locations.csv')

time_series_data_types = config.get_time_series_data_types()

def get_time_series_data_by_type(config_dict):
    time_series_data = {}
    for data_type in time_series_data_types:
        data_type_data = load_data.load_data_type(data_type, config_dict)
        if data_type_data is not None:
            time_series_data[data_type] = data_type_data
    return time_series_data

def get_time_series_df(config_dict):
    joined_df = None
    time_series_data_by_type = get_time_series_data_by_type(config_dict)
    for df in time_series_data_by_type.values():
        if joined_df is None:
            joined_df = df
        else:
            joined_df = joined_df.merge(df, on=['date', 'region_code'], how='outer')
    location_names_df = pd.read_csv(LOCATIONS_PATH)
    location_names_df = location_names_df[['region_code', 'region_name']]
    time_series_df = joined_df.merge(location_names_df, on=['region_code'], how='inner')
    identifier_cols = ['region_code', 'region_name', 'date']
    time_series_df_cols = [c for c in time_series_df.columns if c not in identifier_cols]
    time_series_df = time_series_df[identifier_cols + time_series_df_cols]
    return time_series_df
