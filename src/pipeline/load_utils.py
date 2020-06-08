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
import datetime
import os

import config
import date_utils
from path_utils import ROOT_DIR, most_recent_data


def rename_data_columns(data_df, params):
    rename_dict = config.get_rename_dict(params['data'])
    data_df = data_df.rename(columns=rename_dict)
    return data_df

def default_read_function(params):
    data_path = most_recent_data(params)['path']
    read_params = None
    if 'read' in params['load']:
        read_params = params['load']['read']
    file_extension = params['fetch']['file'].split('.')[1]
    default_args = {
        'csv': {'encoding': None, 'delimiter': None, 'skipfooter': 0},
        'xlsx': {'sheet_name': 0, 'skiprows': None, 'skipfooter': 0}
    }
    read_args = default_args[file_extension]
    if read_params:
        for k in read_args.keys():
            if k in read_params:
                read_args[k] = read_params[k]
    if file_extension == 'csv':
        data_df = pd.read_csv(data_path, delimiter=read_args['delimiter'], encoding=read_args['encoding'], skipfooter=read_args['skipfooter'])
    elif file_extension == 'xlsx':
        data_df = pd.read_excel(data_path, sheet_name=read_args['sheet_name'], skiprows=read_args['skiprows'], skipfooter=read_args['skipfooter'])

    data_df = date_utils.parse_date(data_df, params)
    data_df = rename_data_columns(data_df, params)

    return data_df

def compute_cumulative_from_new(df, params):
    data_columns = params['data']
    schema = config.read_data_schema()
    for data_type in data_columns.keys():
        formats = data_columns[data_type]
        if 'new' in formats and 'cumulative' not in formats:
            cum_col_name = schema[data_type]['columns']['cumulative']
            new_col_name = schema[data_type]['columns']['new']
            df[cum_col_name] = df.sort_values('date').groupby('region_code')[new_col_name].apply(lambda x: x.cumsum())
    return df
