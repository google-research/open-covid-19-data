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
import yaml

import load_utils
import load_functions
import config


config_dict = config.read_config()
data_columns_by_type = config.get_data_columns_by_type()
identifier_columns = config.get_identifier_columns()

def load_data_type(data_type):
    list_of_dfs = []
    for k in config_dict:
        params = config_dict[k]
        if 'data' in params and data_type in params['data']:
            load_func_name = params['load']['function']
            load_func = getattr(load_functions, load_func_name)
            df = load_func(params)
            columns_to_keep = identifier_columns + data_columns_by_type[data_type]
            df = df[df.columns[df.columns.isin(columns_to_keep)]]
            load_params = params['load']
            if 'regions' in load_params and 'omit' in load_params['regions']:
                omit_params = load_params['regions']['omit']
                if data_type in omit_params:
                    omit_regions = omit_params[data_type]
                    df = df[~df.region_code.isin(omit_regions)]
            list_of_dfs.append(df)
    joined = pd.concat(list_of_dfs)
    return joined

def get_file_path(data_path):
    dir = data_path['dir']
    file = data_path['file']
    path = ''
    if 'find_recent' in data_path and data_path['find_recent']:
        path, _ = load_utils.most_recent_data(dir, file)
    else:
        path = os.path.join(dir, file)

    return path

# load data and get the timestamp on filesystem
def load_data_fs_timestamps_by_region():
    column_names = list(data_columns_by_type.keys())
    list_of_dfs = []

    for k in config_dict:
        params = config_dict[k]
        data_types = list(params['data'])
        data_path = get_file_path(params['path'])
        timestamp = load_utils.get_timestamp_from_file(data_path)
        load_func = getattr(load_functions, params['load']['function'])
        df = load_func(params)
        df = df[df.columns[df.columns.isin(identifier_columns)]]
        regions = df.region_code.unique()
        df = pd.DataFrame(columns = column_names)
        df['region_code'] = regions.tolist()
        for dt in data_types:
            df[dt] = timestamp

        list_of_dfs.append(df)


    # combine all data_frames
    result_df = pd.concat(list_of_dfs).fillna('')
    # squash rows of same region together
    agg_funcs = dict.fromkeys(column_names, lambda x: ''.join(x))
    result_df = result_df.groupby(['region_code']).agg(agg_funcs).reset_index()

    return result_df
