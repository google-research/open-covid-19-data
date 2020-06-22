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
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')

EXPORT_PATH_CC_BY = os.path.join(ROOT_DIR, 'data/exports/cc_by/aggregated_cc_by.csv')
EXPORT_PATH_CC_BY_SA = os.path.join(ROOT_DIR, 'data/exports/cc_by_sa/aggregated_cc_by_sa.csv')

sys.path.append(PIPELINE_DIR)

import join_data

time_series_df_cc_by = join_data.get_time_series_df(cc_by_sa=False, google_tos=True)
time_series_df_cc_by.to_csv(EXPORT_PATH_CC_BY, index=False)

time_series_df_cc_by_sa = join_data.get_time_series_df(cc_by_sa=True, google_tos=False)
time_series_df_cc_by_sa.to_csv(EXPORT_PATH_CC_BY_SA, index=False)
