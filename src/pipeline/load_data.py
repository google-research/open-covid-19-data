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

import load_functions
import config


data_columns_by_type = config.get_data_columns_by_type()
identifier_columns = config.get_identifier_columns()

def load_data_type(data_type, config_dict):
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
    if list_of_dfs:
        joined = pd.concat(list_of_dfs)
        return joined
    else:
        return None
