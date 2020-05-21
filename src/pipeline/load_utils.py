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


def rename_data_columns(data_df, params):
    rename_dict = config.get_rename_dict(params['data'])
    data_df = data_df.rename(columns=rename_dict)
    return data_df

def default_read_function(params):
    source_params = params['path']
    read_params = None
    if 'read' in params['load']:
        read_params = params['load']['read']
    data_path, _ = most_recent_data(source_params['dir'], source_params['file'])
    file_extension = source_params['file'].split('.')[1]
    default_args = {
        'csv': {'encoding': None, 'delimiter': None},
        'xlsx': {'sheet_name': 0, 'skiprows': None, 'skipfooter': 0}
    }
    read_args = default_args[file_extension]
    if read_params:
        for k in read_args.keys():
            if k in read_params:
                read_args[k] = read_params[k]
    if file_extension == 'csv':
        data_df = pd.read_csv(data_path, delimiter=read_args['delimiter'], encoding=read_args['encoding'])
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

# Returns path, date
def most_recent_data(directory, file):
    dir_abs_path = os.path.abspath(os.path.join(os.path.join(__file__, '../../..'), directory))
    _, subdirs, _ = next(os.walk(dir_abs_path))
    subdirs_that_are_dates = []
    for sd in subdirs:
        try:
            sd_date = datetime.datetime.strptime(sd, '%Y-%m-%d').date()
            subdirs_that_are_dates.append(sd_date)
        except ValueError:
            continue
    sorted_subdir_dates = sorted(subdirs_that_are_dates, reverse=True)
    for subdir_date in sorted_subdir_dates:
        date_str = subdir_date.strftime("%Y-%m-%d")
        path_to_file = os.path.join(dir_abs_path, date_str, file)
        if os.path.exists(path_to_file):
            return path_to_file, subdir_date
    return 'file path contains no data', 'file path contains no data'

def get_timestamp_from_file(path):
    if not os.path.exists(path):
        return 'invald file path'
    m_time = os.path.getmtime(path)
    formatted_timestamp = datetime.datetime.fromtimestamp(m_time)
    formatted_timestamp = formatted_timestamp.strftime('%Y-%m-%d')
    return formatted_timestamp
