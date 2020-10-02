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


# Test that data directories are on the allowlist
def test_data_is_allowed():
    sources_with_data = config.get_sources_with_data()
    allowlist = config.read_allowlist()
    for source in sources_with_data:
        assert source in allowlist

# Test that yaml files for config sources are on the allowlist
def test_source_files_are_allowlisted():
    allowlist = config.read_allowlist()
    for source_file_name in os.listdir(path_utils.path_to('sources_dir')):
        source_key = os.path.splitext(source_file_name)[0]
        assert source_key in allowlist

# Test that downloaded and scraped inputs are on the allowlist
def test_inputs_are_allowlisted():
    allowlist = config.read_allowlist()
    for source_file_name in os.listdir(path_utils.path_to('downloaded_dir')):
        source_key = os.path.splitext(source_file_name)[0]
        assert source_key in allowlist

    for source_file_name in os.listdir(path_utils.path_to('scraped_dir')):
        if source_file_name == 'spreadsheets':
          continue
        source_key = os.path.splitext(source_file_name)[0]
        assert source_key in allowlist
