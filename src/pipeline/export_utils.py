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
import join_data
import config
import load_data
import pandas as pd
import numpy as np
import region_utils


def export_data(config_dict=None, export_path=None):
    aggregated_config_dict = config.filter_by_aggregate_data(config_dict, aggregate_data=True)
    non_aggregated_config_dict = config.filter_by_aggregate_data(config_dict, aggregate_data=False)
    export_aggregated_data(aggregated_config_dict, export_path)
    export_non_aggregated_data(non_aggregated_config_dict, export_path)

def export_aggregated_data(config_dict, export_path):
    time_series_df = join_data.get_time_series_df(config_dict)
    if time_series_df is None:
        logging.warning('time_series_df is None, will not export to %s. config_dict keys: %s',
                        export_path, config_dict.keys())
    else:
        time_series_df = time_series_df.rename(columns={'region_code': 'open_covid_region_code'})
        time_series_df.to_csv(export_path, index=False)

# Hack: This function breaks most of the abstractions around load_functions
# because the load function on non-aggregated data has side effects that directly
# write the exported csv instead of returning it here. Also, this export_path arg is never consumed.
def export_non_aggregated_data(config_dict, export_path):
    print('export path (not used): ', export_path)
    for key in config_dict.keys():
        load_data.load_most_recent_loadable_data(config_dict[key])
    print(config_dict.keys())

def write_csv_with_open_covid_region_code_added(input_path, output_path):
    print('input path: ', input_path, ', output_path: ', output_path)
    input_df = pd.read_csv(input_path)
    output_df = input_df.copy()

    # Location columns have different names than mobility data,
    # transform here so can reuse join_mobility_region_codes()
    column_renames = {}
    if 'iso_3166_2_code' not in output_df:
        column_renames['sub_region_1_code'] = 'iso_3166_2_code'
    if 'census_fips_code' not in output_df:
        column_renames['sub_region_2_code'] = 'census_fips_code'
    output_df = output_df.rename(columns=column_renames)

    if 'metro_area' not in output_df:
        output_df['metro_area'] = np.nan

    input_num_rows = len(input_df)
    output_df = region_utils.join_mobility_region_codes(output_df, None)
    output_num_rows = len(output_df)
    print('INPUT ROWS: ', input_num_rows, ', OUTPUT ROWS: ', output_num_rows)
    # assert input_num_rows == output_num_rows

    reversed_column_renames = {v: k for (k, v) in column_renames.items()}
    reversed_column_renames['region_code'] = 'open_covid_region_code'

    output_df = output_df.rename(columns=reversed_column_renames)
    output_columns = ['open_covid_region_code'] + list(input_df.columns)
    output_df = output_df[output_columns]
    output_df.to_csv(output_path, index=False)
