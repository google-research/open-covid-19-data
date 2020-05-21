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


import os
import pandas as pd

import region_utils
import load_utils
import date_utils


def default_load_function(params):
    df = load_utils.default_read_function(params)
    df = region_utils.join_from_params(df, params)
    load_params = params['load']
    if 'regions' in load_params:
        if 'aggregate_by' in load_params['regions']:
            df = region_utils.aggregate_and_append(df, params)
    df = load_utils.compute_cumulative_from_new(df, params)
    return df

def covidtracking(params):
    data_df = default_load_function(params)
    data_df = data_df.reindex(index=data_df.index[::-1])
    return data_df

# Note: we only include regions that are computing cumulative hospitalizations
# and don't compute a country-level hospitalization number for Spain
def spain_and_regions(params):
    data_df = default_load_function(params)
    data_df = data_df[
        (data_df['source_region_name'] != 'Castilla y León') &
        (data_df['source_region_name'] != 'Castilla La Mancha') &
        (data_df['source_region_name'] != 'C. Valenciana') &
        (data_df['source_region_name'] != 'Madrid') &
        (data_df['source_region_name'] != 'Cataluña')
    ]
    return data_df

def japan_hospitalizations(params):
    data_df = load_utils.default_read_function(params)
    data_df['deaths_cumulative'] = data_df['deaths_cumulative'].replace(to_replace='-', value=0).astype('int32')
    data_df = region_utils.join_from_params(data_df, params)
    data_df = region_utils.aggregate_and_append(data_df, params)
    return data_df

def netherlands_hospitalizations(params):
    df = default_load_function(params)
    df = df.rename(columns={
        'nieuw': 'new_reports',
        'tot en met gisteren': 'reported_through_yesterday'
    })
    df['hospitalized_current'] = df['new_reports'] + df['reported_through_yesterday']
    return df

# Tricky because hospitalization data for scotland data comes from UK
# data source, but ICU data comes from here. Make sure they get joined correctly.
def scotland_hospitalizations(params):
    data_path, _ = load_utils.most_recent_data(params['path']['dir'], params['path']['file'])
    df = pd.read_excel(data_path, 'Table 2 - Hospital Care', skiprows=4)
    df = df.rename(columns={
        df.columns[1]: "icu_current",
        df.columns[4]: "hospitalized_current",
    })
    df = date_utils.parse_date(df, params)
    df = region_utils.join_from_params(df, params)
    return df
