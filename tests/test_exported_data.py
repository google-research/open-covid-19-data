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
import pandas as pd
import sys
import streamlit as st

PIPELINE_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')), 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import path_utils

AGGREGATED_EXPORT_FILES = ['cc_by/aggregated_cc_by.csv',
                'cc_by_sa/aggregated_cc_by_sa.csv',
                'cc_by_nc/aggregated_cc_by_nc.csv']

def test_location_and_date_unique():
    for f in AGGREGATED_EXPORT_FILES:
        export_path = os.path.join(path_utils.path_to('export_dir'), f)
        exported_df = pd.read_csv(export_path)
        duplicates = exported_df[exported_df[['open_covid_region_code', 'date']].duplicated(keep=False)]
        duplicate_info = duplicates[['open_covid_region_code', 'date']]
        print(duplicate_info)
        assert duplicates.shape[0] == 0

test_location_and_date_unique()
