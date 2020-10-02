# Copyright 2020 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml
import os

DATA_YAML = os.path.abspath(os.path.join(__file__, '../../config/data.yaml'))
ALLOWLIST_YAML = os.path.abspath(os.path.join(__file__, '../../config/allowlist.yaml'))
SOURCES_DIR = os.path.abspath(os.path.join(__file__, '../../config/sources'))
DATA_INPUTS_DIR = os.path.abspath(os.path.join(__file__, '../../../data/inputs/'))

def read_data_schema():
    with open(DATA_YAML) as file:
        schema = yaml.load(file, Loader=yaml.FullLoader)
    return schema

def all_data_schema_columns():
    column_list = []
    schema = read_data_schema()
    for data_type in schema.values():
        columns = data_type['columns']
        column_values = list(columns.values())
        column_list.extend(column_values)
    return column_list

def read_allowlist():
    with open(ALLOWLIST_YAML) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def all_region_columns():
    return ['region_code'] + other_region_columns()

def other_region_columns():
    return ['parent_region_code',
            'region_code_type',
            'region_code_level',
            'level_1_region_code',
            'level_2_region_code',
            'level_3_region_code']

def get_sources_with_data():
    downloaded_dir = os.path.join(DATA_INPUTS_DIR, 'downloaded')
    scraped_dir = os.path.join(DATA_INPUTS_DIR, 'scraped')
    downloaded_sources = [f.name for f in os.scandir(downloaded_dir) if f.is_dir()]
    scraped_sources = [f.name for f in os.scandir(scraped_dir) if f.is_dir()]
    scraped_sources.remove('spreadsheets')
    result = downloaded_sources + scraped_sources
    return result

def read_config(cc_by=True,
                cc_by_sa=False,
                cc_by_nc=False,
                google_tos=False,
                filter_no_load_func=True,
                filter_no_data=True,
                filter_not_approved=True,
                filter_by_fetch_method=None):
    config_dict = {}
    allowlist = read_allowlist()
    sources_with_data = get_sources_with_data()
    for source_file_name in os.listdir(SOURCES_DIR):
        source_file = os.path.join(SOURCES_DIR, source_file_name)
        source_key = os.path.splitext(source_file_name)[0]
        if filter_not_approved and source_key not in allowlist:
            continue
        with open(source_file) as file:
            params = yaml.load(file, Loader=yaml.FullLoader)
        params['config_key'] = source_key
        # pylint: disable=bad-continuation
        if ((filter_no_load_func
             and ('load' not in params or 'function' not in params['load'] or params['load']['function'] is None))
            or (filter_by_fetch_method
                and ('fetch' not in params or params['fetch']['method'] != filter_by_fetch_method))
            or (filter_no_data and (source_key not in sources_with_data))
            or (not cc_by and params['license']['cc_by'])
            or (not cc_by_sa and params['license']['cc_by_sa'])
            or (not cc_by_nc and params['license']['cc_by_nc'])
            or (not google_tos and params['license']['google_tos'])):
            continue
        # pylint: enable=bad-continuation
        config_dict[source_key] = params
    return config_dict

def col_params_to_col_list(data_columns_params):
    data_schema = read_data_schema()
    column_list = []
    for data_type in data_columns_params.keys():
        data_type_formats = data_columns_params[data_type]
        schema_cols = data_schema[data_type]['columns']
        for data_type_format in data_type_formats:
            col_name = schema_cols[data_type_format]
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
        for data_format in data_columns[data_type].keys():
            our_col_name = schema[data_type]['columns'][data_format]
            source_col_name = data_columns[data_type][data_format]
            rename_dict[source_col_name] = our_col_name
    return rename_dict

# Returns config dict where load.aggregate_data field matches aggregate_data arg.
# Note that config sources with no load field are not returned in either case.
def filter_by_aggregate_data(config_dict, aggregate_data=True):
    filtered_dict = {
        source: params for (source, params) in config_dict.items()
        if 'load' in params and params['load']['aggregate_data'] == aggregate_data
    }
    return filtered_dict
