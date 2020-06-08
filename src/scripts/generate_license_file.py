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
import sys
import yaml

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')
LICENSE_PATH = os.path.join(ROOT_DIR, 'LICENSE')

sys.path.append(PIPELINE_DIR)

import config

sources = config.read_config(filter_no_load_func=False)

with open(LICENSE_PATH, 'w') as out:
    for key in sources:
        source_params = sources[key]
        print(source_params)
        if 'license' in source_params:
            out.write(source_params['attribution']['country'] + '\n')
            out.write('License: ')
            out.write(source_params['license']['name'] + '\n')
            out.write('Link: ')
            out.write(source_params['license']['link'] + '\n\n')
            out.write('==================================================')
            out.write('\n\n')
