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

import streamlit as st
import pandas as pd
import os
import sys

PIPELINE_DIR = os.path.join(os.path.dirname(__file__), '../../../', 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import path_utils


# Load FIPS codes as strings so you don't lose the leading zeros
fips_df = pd.read_csv(os.path.join(path_utils.path_to('locations_intermediate_dir'), 'fips_locations.csv'), dtype=str)
iso_level_1_df = pd.read_csv(os.path.join(path_utils.path_to('locations_intermediate_dir'), 'iso_3166_1_locations.csv'))
iso_level_2_df = pd.read_csv(os.path.join(path_utils.path_to('locations_intermediate_dir'), 'iso_3166_2_locations.csv'))
other_df = pd.read_csv(os.path.join(path_utils.path_to('locations_intermediate_dir'), 'other_locations.csv'))

concat_df = pd.concat([fips_df, iso_level_1_df, iso_level_2_df, other_df])
st.write(concat_df)

concat_df.to_csv(path_utils.path_to('locations_csv'), index=False)
print('Wrote concatenated locations file to %s.' % path_utils.path_to('locations_csv'))
