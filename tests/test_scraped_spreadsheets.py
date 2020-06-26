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
import datetime
import pandas as pd
import sys

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')
SPREADSHEET_DIR = os.path.join(ROOT_DIR, 'data/inputs/scraped/spreadsheets')

sys.path.append(PIPELINE_DIR)

import config


# All subdirectories within SPREADSHEET_DIR should be named
# as '%Y-%m-%d' dates
def test_spreadsheet_dates():
    _, subdirs, _ = next(os.walk(SPREADSHEET_DIR))
    print(subdirs)
    for subdir in subdirs:
        try:
            sd_date = datetime.datetime.strptime(subdir, '%Y-%m-%d')
        except ValueError:
            print('Okay value error', subdir)
            assert False, 'The subdirectory name {} in {} must be formatted as a YYYY-MM-DD date.'.format(
                subdir, SPREADSHEET_DIR)

# Each subdirectory within SPREADSHEET_DIR should contain
# exactly one file named 'hospitalizations.xlsx'
def test_spreadsheet_subdirectory_contents():
    dirpath, subdirs, filenames = next(os.walk(SPREADSHEET_DIR))
    for subdir in subdirs:
        subdir_path = os.path.join(dirpath, subdir)
        dir_contents = os.listdir(subdir_path)
        print(subdir_path, dir_contents)
        assert len(dir_contents) == 1, 'The directory {} should contain exactly one file.'.format(subdir_path)
        print(dir_contents[0])
        assert dir_contents[0] == 'hospitalizations.xlsx', \
            'The file in directory {} should be named `hospitalizations.xlsx`.'.format(subdir_path)

# Each hospitalizations.xlsx spreadsheet should contain only tabs
# where the tab names are on the whitelist
def test_spreadsheet_tabs_against_whitelist():
    whitelist = config.read_whitelist()
    dirpath, subdirs, filenames = next(os.walk(SPREADSHEET_DIR))
    for subdir in subdirs:
        subdir_path = os.path.join(dirpath, subdir)
        hosp_file = os.path.join(subdir_path, 'hospitalizations.xlsx')
        xl = pd.ExcelFile(hosp_file)
        sheet_names = xl.sheet_names
        print('File: ', hosp_file)
        print('Sheet names in spreadsheet: ', sheet_names)
        print('Sheet names allowed in whitelist: ', whitelist)
        assert set(sheet_names).issubset(set(whitelist)), \
            "Spreadsheet {} contains a sheet name that is not on the whitelist.".format(hosp_file)

# Columns in the spreadsheets should only be names that exist in data.yaml
def test_spreadsheet_column_names_against_schema():
    allowed_data_columns = config.all_data_schema_columns()
    dirpath, subdirs, filenames = next(os.walk(SPREADSHEET_DIR))
    for subdir in subdirs:
        subdir_path = os.path.join(dirpath, subdir)
        hosp_file = os.path.join(subdir_path, 'hospitalizations.xlsx')
        xl = pd.ExcelFile(hosp_file)
        sheet_names = xl.sheet_names
        for s in sheet_names:
            df = xl.parse(s, nrows=2)
            print(df)
            columns_in_spreadsheet = list(df.columns)
            assert 'date' in columns_in_spreadsheet, \
                'Spreadsheet {} and sheet {} must have a column named "date".'.format(hosp_file, s)
            columns_in_spreadsheet.remove('date')
            print(columns_in_spreadsheet)
            print(allowed_data_columns)
            assert set(columns_in_spreadsheet).issubset(allowed_data_columns)
