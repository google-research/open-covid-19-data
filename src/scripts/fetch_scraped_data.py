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
import yaml
import os
import sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import load_utils

with open(os.path.join(ROOT_DIR, 'src/config/sources.yaml')) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

spreadsheet_dir = os.path.join(ROOT_DIR, 'data/inputs/scraped/spreadsheets')
spreadsheet_file = 'hospitalizations.xlsx'

path, date = load_utils.most_recent_data(spreadsheet_dir, spreadsheet_file)
print(path)

# This assumes that every data source with scraped: True in sources.yaml comes from a single spreadsheet.
# If that stops being the case, will need to update this.

todays_date = datetime.today().strftime('%Y-%m-%d')

for k in config:
    params = config[k]
    if params['fetch']['scraped']:
        df = pd.read_excel(path, k)
        out_dir = os.path.join(ROOT_DIR, params['path']['dir'], todays_date)
        out_file = params['path']['file']
        out_path = os.path.join(out_dir, out_file)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        df.to_csv(out_path, index=False)
