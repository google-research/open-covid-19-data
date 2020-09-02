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
import numpy as np
import logging
import os

import region_utils
import load_utils
import date_utils
import path_utils
import export_utils
import shutil


def default_load_function(data_path, params):
    df = load_utils.default_read_function(data_path, params)
    df = region_utils.join_region_codes(df, params)
    duplicates = df[df[['region_code', 'date']].duplicated(keep=False)]
    if duplicates.shape[0] != 0:
        logging.warning('Dropping the following duplicate data for %s data source:\n%s',
                        params['config_key'], duplicates[['region_code', 'date']])
        df = df.drop_duplicates(subset=['region_code', 'date'], keep='first')
    load_params = params['load']
    if 'regions' in load_params:
        if 'aggregate_by' in load_params['regions']:
            df = region_utils.aggregate_and_append(df, params)
    df = load_utils.compute_cumulative_from_new(df, params)
    return df

def nytimes_load_function(data_path, params):
    df = load_utils.default_read_function(data_path, params)
    df = region_utils.join_nytimes_region_codes(df, params)
    return df

def mobility_load_function(data_path, params):
    df = load_utils.default_read_function(data_path, params)
    df = region_utils.join_mobility_region_codes(df, params)
    return df

# This function has side effects (writing to the export directory)
def google_load_function(data_path, params):
    input_dir = os.path.dirname(data_path)
    export_dir = os.path.join(path_utils.path_to('export_dir'), params['config_key'])
    print('input dir: ', input_dir)
    print('export dir: ', export_dir)
    for path, subdirs, files in os.walk(input_dir):
        print('path: ', path)
        for subdir in subdirs:
            print('subdir: ', subdir)
            export_subdir_path = os.path.join(export_dir,
                                              os.path.relpath(os.path.join(path, subdir), start=input_dir))
            if not os.path.exists(export_subdir_path):
                print('making subdir: ', export_subdir_path)
                os.makedirs(export_subdir_path)
        for file in files:
            file_path = os.path.join(path, file)
            print('file_path: ', file_path)
            rel_path = os.path.relpath(file_path, start=input_dir)
            print('rel path: ', rel_path)
            export_path = os.path.join(export_dir, rel_path)
            if os.path.basename(file).endswith('.csv'):
                export_utils.write_csv_with_open_covid_region_code_added(file_path, export_path)
            if file.endswith('.md'):
                shutil.copyfile(file_path, export_path)

def covidtracking(data_path, params):
    data_df = default_load_function(data_path, params)
    data_df = data_df.reindex(index=data_df.index[::-1])
    return data_df

# Note: we only include regions that are computing cumulative hospitalizations
# and don't compute a country-level hospitalization number for Spain
# pylint: disable=bad-continuation
def spain_and_regions(data_path, params):
    data_df = default_load_function(data_path, params)
    data_df['hospitalized_current'] = data_df.apply(
        lambda row: (row['hospitalized_cumulative']
            if ((row['local_alpha_code'] == 'CM' and row['date'] < '2020-04-11')
                or (row['local_alpha_code'] == 'MD' and row['date'] < '2020-04-26'))
            else np.nan), axis=1
    )
    data_df['hospitalized_cumulative'] = data_df.apply(
        lambda row: row['hospitalized_cumulative'] if pd.isnull(row['hospitalized_current']) else np.nan, axis=1
    )
    data_df['icu_current'] = data_df.apply(
        lambda row: (row['icu_cumulative']
            if ((row['local_alpha_code'] == 'CL' and row['date'] < '2020-04-17')
                or (row['local_alpha_code'] == 'GA' and row['date'] < '2020-04-28')
                or (row['local_alpha_code'] == 'CM' and row['date'] < '2020-04-12')
                or (row['local_alpha_code'] == 'MD' and row['date'] < '2020-04-26'))
            else np.nan), axis=1
    )
    data_df['icu_cumulative'] = data_df.apply(
        lambda row: row['icu_cumulative'] if pd.isnull(row['icu_current']) else np.nan, axis=1
    )
    return data_df
# pylint: enable=bad-continuation

def japan_hospitalizations(data_path, params):
    data_df = load_utils.default_read_function(data_path, params)
    data_df['deaths_cumulative'] = data_df['deaths_cumulative'].replace(to_replace='-', value=0).astype('int32')
    data_df = region_utils.join_region_codes(data_df, params)
    data_df = region_utils.aggregate_and_append(data_df, params)
    return data_df

def netherlands_hospitalizations(data_path, params):
    df = default_load_function(data_path, params)
    df = df.rename(columns={
        'nieuw': 'new_reports',
        'tot en met gisteren': 'reported_through_yesterday'
    })
    df['hospitalized_current'] = df['new_reports'] + df['reported_through_yesterday']
    return df

# Tricky because hospitalization data for scotland data comes from UK
# data source, but ICU data comes from here. Make sure they get joined correctly.
def scotland_hospitalizations(data_path, params):
    df = pd.read_excel(data_path, 'Table 2 - Hospital Care', skiprows=4)
    df = df.rename(columns={
        df.columns[1]: 'icu_current',
        df.columns[4]: 'hospitalized_current',
    })
    df = date_utils.parse_date(df, params)
    df = region_utils.join_region_codes(df, params)
    return df
