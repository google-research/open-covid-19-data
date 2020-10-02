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

import os
import datetime
import pandas as pd
import sys

PIPELINE_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')), 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import config
import path_utils


# All subdirectories within spreadsheets_dir should be named as '%Y-%m-%d' dates.
def test_spreadsheet_dates():
    _, subdirs, _ = next(os.walk(path_utils.path_to('spreadsheets_dir')))
    print(subdirs)
    for subdir in subdirs:
        try:
            sd_date = datetime.datetime.strptime(subdir, '%Y-%m-%d')
        except ValueError:
            print('Okay value error', subdir)
            assert False, 'The subdirectory name {} in {} must be formatted as a YYYY-MM-DD date.'.format(
                subdir, path_utils.path_to('spreadsheets_dir'))

# Each subdirectory within spreadsheets_dir should contain exactly one file named 'hospitalizations.xlsx'.
def test_spreadsheet_subdirectory_contents():
    dirpath, subdirs, filenames = next(os.walk(path_utils.path_to('spreadsheets_dir')))
    for subdir in subdirs:
        subdir_path = os.path.join(dirpath, subdir)
        dir_contents = os.listdir(subdir_path)
        print(subdir_path, dir_contents)
        assert len(dir_contents) == 1, 'The directory {} should contain exactly one file.'.format(subdir_path)
        print(dir_contents[0])
        assert dir_contents[0] == 'hospitalizations.xlsx', \
            'The file in directory {} should be named `hospitalizations.xlsx`.'.format(subdir_path)

# Each hospitalizations.xlsx spreadsheet should contain only tabs
# where the tab names are on the allowlist
def test_spreadsheet_tabs_against_allowlist():
    allowlist = config.read_allowlist()
    dirpath, subdirs, filenames = next(os.walk(path_utils.path_to('spreadsheets_dir')))
    for subdir in subdirs:
        subdir_path = os.path.join(dirpath, subdir)
        hosp_file = os.path.join(subdir_path, 'hospitalizations.xlsx')
        xl = pd.ExcelFile(hosp_file)
        sheet_names = xl.sheet_names
        print('File: ', hosp_file)
        print('Sheet names in spreadsheet: ', sheet_names)
        print('Sheet names allowed in allowlist: ', allowlist)
        for sheet in sheet_names:
            assert sheet in allowlist, \
            "Spreadsheet {} contains a sheet name {} that is not on the allowlist.".format(hosp_file, sheet)

# Columns in the spreadsheets should only be names that exist in data.yaml
def test_spreadsheet_column_names_against_schema():
    allowed_data_columns = config.all_data_schema_columns()
    dirpath, subdirs, filenames = next(os.walk(path_utils.path_to('spreadsheets_dir')))
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
            for column in columns_in_spreadsheet:
                assert column in allowed_data_columns, \
                    'Sheet {} in spreadsheet {} contains the column {}, which is not a column name' + \
                    'recognized by data.yaml'.format(s, hosp_file, column)
