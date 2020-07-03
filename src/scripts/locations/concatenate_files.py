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

import streamlit as st
import pandas as pd
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../../'))
LOCATIONS_INTERMEDATE_DIR = os.path.join(ROOT_DIR, 'data/inputs/static/locations/intermediate')
LOCATIONS_EXPORT_DIR = os.path.join(ROOT_DIR, 'data/exports/locations')
LOCATIONS_PATH = os.path.join(LOCATIONS_EXPORT_DIR, 'locations.csv')

# Load FIPS codes as strings so you don't lose the leading zeros
fips_df = pd.read_csv(os.path.join(LOCATIONS_INTERMEDATE_DIR, 'fips_locations.csv'), dtype=str)
iso_level_1_df = pd.read_csv(os.path.join(LOCATIONS_INTERMEDATE_DIR, 'iso_3166_1_locations.csv'))
iso_level_2_df = pd.read_csv(os.path.join(LOCATIONS_INTERMEDATE_DIR, 'iso_3166_2_locations.csv'))
other_df = pd.read_csv(os.path.join(LOCATIONS_INTERMEDATE_DIR, 'other_locations.csv'))

concat_df = pd.concat([fips_df, iso_level_1_df, iso_level_2_df, other_df])
st.write(concat_df)

concat_df.to_csv(LOCATIONS_PATH, index=False)
print('Wrote concatenated locations file to %s.' % LOCATIONS_PATH)
