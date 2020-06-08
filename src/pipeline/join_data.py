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


time_series_data_types = config.get_time_series_data_types()

def get_time_series_data_by_type(cc_by_sa=False):
    time_series_data = {}
    for dt in time_series_data_types:
        time_series_data[dt] = load_data.load_data_type(dt, cc_by_sa)
    return time_series_data

def get_time_series_df(cc_by_sa=False):
    joined_df = None
    time_series_data_by_type = get_time_series_data_by_type(cc_by_sa)
    for df in time_series_data_by_type.values():
        if joined_df is None:
            joined_df = df
        else:
            joined_df = joined_df.merge(df, on=['date', 'region_code'], how='outer')
    locations_path = os.path.abspath(os.path.join(__file__, '../../..', 'data/inputs/static/locations.csv'))
    locations_df = pd.read_csv(locations_path)
    locations_df = locations_df[['region_code', 'region_name']]
    time_series_df = joined_df.merge(locations_df, on=['region_code'], how='inner')
    identifier_cols = ['region_code', 'region_name', 'date']
    time_series_df_cols = [c for c in time_series_df.columns if c not in identifier_cols]
    time_series_df = time_series_df[identifier_cols + time_series_df_cols]
    return time_series_df
