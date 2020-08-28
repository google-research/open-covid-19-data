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
import pandas as pd
import sys

PIPELINE_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')), 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import path_utils

LOCATIONS_INTERMEDIATE_FILES = ['fips_locations.csv', 'iso_3166_1_locations.csv', 'iso_3166_2_locations.csv', 'other_locations.csv']


def test_locations_unique():
    locations_df = pd.read_csv(path_utils.path_to('locations_csv'))
    location_duplicates = locations_df[locations_df['region_code'].duplicated(keep=False)]
    print(location_duplicates)
    assert location_duplicates.shape[0] == 0

def test_intermediate_locations_unique():
    for f in LOCATIONS_INTERMEDIATE_FILES:
        loc_path = os.path.join(path_utils.path_to('locations_intermediate_dir'), f)
        locations_df = pd.read_csv(loc_path)
        location_duplicates = locations_df[locations_df['region_code'].duplicated(keep=False)]
        print(location_duplicates)
        assert location_duplicates.shape[0] == 0
