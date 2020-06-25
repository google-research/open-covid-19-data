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

import logging
import os
import sys
import wget  # pip3 install python3-wget, not pip install wget
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import args_utils
import path_utils
import config


args = args_utils.get_parser().parse_args()

if not args.whitelist:
    logging.warning('RUNNING WITHOUT THE WHITELIST! DO NOT MAKE A PULL REQUEST WITH THE OUTPUT!')

# Iterate through all the sources, and for anything that is an AUTOMATIC_DOWNLOAD
# get the file from the source url and store it at the desired path.

automatic_downloads = config.read_config(
    filter_by_fetch_method='AUTOMATIC_DOWNLOAD', filter_no_load_func=False, filter_not_approved=args.whitelist)
todays_date = datetime.today().strftime('%Y-%m-%d')

for k in automatic_downloads:
    params = automatic_downloads[k]
    source_url = params['fetch']['source_url']
    if not path_utils.has_data_from_date(params, todays_date):
        path_for_today = path_utils.path_to_data_for_date(params, todays_date)
        print('Downloading data for: ', k)
        print('Source url: ', source_url)
        out_dir = path_for_today['dir']
        out_file = path_for_today['file']
        out_path = os.path.join(out_dir, out_file)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        output = wget.download(source_url, out_path)
        print('\nFile written to: ', output)

print('Done with fetch_automatic_downloads.py')
