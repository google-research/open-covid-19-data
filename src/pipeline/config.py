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
import os

DATA_YAML = os.path.abspath(os.path.join(__file__, '../../config/data.yaml'))
SOURCES_DIR = os.path.abspath(os.path.join(__file__, '../../config/sources'))


def read_data_schema():
    with open(DATA_YAML) as file:
        schema = yaml.load(file, Loader=yaml.FullLoader)
    return schema

def all_region_columns():
    return ['region_code'] + other_region_columns()

def other_region_columns():
    return ['parent_region_code', 'region_code_type', 'region_code_level', 'level_1_region_code', 'level_2_region_code', 'level_3_region_code']

def read_config(cc_by_sa=False, filter_no_load_func=True, filter_not_approved=True, filter_by_fetch_method=None):
    config_dict = {}
    for source_file_name in os.listdir(SOURCES_DIR):
        source_file = os.path.join(SOURCES_DIR, source_file_name)
        with open(source_file) as file:
            params = yaml.load(file, Loader=yaml.FullLoader)
        source_key = os.path.splitext(source_file_name)[0]
        params['config_key'] = source_key
        if (filter_no_load_func and ('load' not in params or 'function' not in params['load'] or params['load']['function'] is None)) or \
            (filter_not_approved and not params['approved']) or \
            (filter_by_fetch_method and params['fetch']['method'] != filter_by_fetch_method) or \
            (not cc_by_sa and params['cc-by-sa']):
            continue
        else:
            config_dict[source_key] = params
    return config_dict

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
