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
SOURCES_DIR = os.path.join(ROOT_DIR, 'src/config/sources')

sys.path.append(PIPELINE_DIR)

import config

# Test that data directories are on the whitelist
def test_data_is_whitelisted():
    sources_with_data = config.get_sources_with_data()
    whitelist = config.read_whitelist()
    for source in sources_with_data:
        assert source in whitelist

# Test that yaml files for config sources are on the whitelist
def test_source_files_are_whitelist():
    whitelist = config.read_whitelist()
    for source_file_name in os.listdir(SOURCES_DIR):
        source_key = os.path.splitext(source_file_name)[0]
        assert source_key in whitelist
