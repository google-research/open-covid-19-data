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

import logging
import pandas as pd

import load_functions
import config
import path_utils


data_columns_by_type = config.get_data_columns_by_type()
identifier_columns = config.get_identifier_columns()

def load_most_recent_loadable_data(params):
    config_key = params['config_key']
    load_func_name = params['load']['function']
    load_func = getattr(load_functions, load_func_name)
    all_data_sorted = path_utils.all_data_most_to_least_recent(params)
    df = None
    for data_dict in all_data_sorted:
        data_path = data_dict['path']
        data_date = data_dict['date']
        try:
            df = load_func(data_path, params)
            logging.warning('Loading succeeded on source %s for date %s', config_key, data_date)
            break
        except Exception as e:  # pylint: disable=broad-except
            logging.warning('Loading failed on source %s for date %s', config_key, data_date)
            logging.warning('    with Exception: %s', str(e))
            continue
    if df is None:
        logging.error(
            'Loading failed for all subdirs for source %s. load_most_recent_loadable_data will return None.',
            config_key)
    return df

def load_data_type(data_type, config_dict):
    list_of_dfs = []
    for k in config_dict:
        params = config_dict[k]
        if 'data' in params and data_type in params['data']:
            df = load_most_recent_loadable_data(params)
            if df is not None:
                columns_to_keep = identifier_columns + data_columns_by_type[data_type]
                df = df[df.columns[df.columns.isin(columns_to_keep)]]
                load_params = params['load']
                if 'regions' in load_params and 'omit' in load_params['regions']:
                    omit_params = load_params['regions']['omit']
                    if data_type in omit_params:
                        omit_regions = omit_params[data_type]
                        df = df[~df.region_code.isin(omit_regions)]
                list_of_dfs.append(df)
    if len(list_of_dfs) > 0:
        joined = pd.concat(list_of_dfs)
        return joined
    else:
        logging.info('Data type %s did not load any data. load_data_type will return None.', data_type)
        return None
