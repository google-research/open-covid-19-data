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

import yaml
from os import path


def read_data_schema():
    p = path.abspath(path.join(__file__, '../../config/data.yaml'))
    with open(p) as file:
        schema = yaml.load(file, Loader=yaml.FullLoader)
    return schema

def read_config(filter_no_load_func=True, filter_not_approved=True):
    p = path.abspath(path.join(__file__, '../../config/sources.yaml'))
    with open(p) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    if filter_no_load_func:
        config = dict(filter(lambda elem: elem[1]['load']['function'] is not None, config.items()))
    if filter_not_approved:
        config = dict(filter(lambda elem: elem[1]['approved'], config.items()))
    return config

def col_params_to_col_list(data_columns_params):
    data_schema = read_data_schema()
    column_list = []
    for data_type in data_columns_params.keys():
        data_type_formats = data_columns_params[data_type]
        schema_cols = data_schema[data_type]['columns']
        for format in data_type_formats:
            col_name = schema_cols[format]
            column_list.append(col_name)
    return column_list

def get_data_columns_by_type():
    data_columns_by_type = {}
    schema = read_data_schema()
    for data_type in schema.keys():
        columns = list(schema[data_type]['columns'].values())
        data_columns_by_type[data_type] = columns
    return data_columns_by_type

def get_identifier_columns():
    return ['date', 'region_code']

def get_time_series_data_types():
    schema = read_data_schema()
    time_series_data_types_dict = dict(filter(lambda elem: elem[1]['time_series'], schema.items()))
    time_series_data_types = list(time_series_data_types_dict.keys())
    return time_series_data_types

def get_rename_dict(data_columns):
    schema = read_data_schema()
    rename_dict = {}
    for data_type in data_columns.keys():
        for format in data_columns[data_type].keys():
            our_col_name = schema[data_type]['columns'][format]
            source_col_name = data_columns[data_type][format]
            rename_dict[source_col_name] = our_col_name
    return rename_dict
