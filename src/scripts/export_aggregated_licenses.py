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

EXPORT_PATH_CC_BY_LICENSE = os.path.join(ROOT_DIR, 'data/exports/cc_by/LICENSE')
EXPORT_PATH_CC_BY_SA_LICENSE = os.path.join(ROOT_DIR, 'data/exports/cc_by_sa/LICENSE')

sys.path.append(PIPELINE_DIR)

import config

cc_by_header = '''The file `aggregated_cc_by.csv` is licensed under Creative Commons Attribution 4.0 International.\n
It includes content under the following licenses:\n\n'''
cc_by_sa_header = '''The file `aggregated_cc_by_sa.csv` is licensed under Creative Commons Attribution-ShareAlike 4.0 International.\n
It includes content under the following licenses:\n\n'''

complete_texts = '''Complete license texts for each unique license are available below:\n\n'''

config_dict_cc_by = config.read_config(cc_by_sa=False)
config_dict_cc_by_sa = config.read_config(cc_by_sa=True)

all_license_files_cc_by = ['docs/license_files/cc-by-4.0']
all_license_files_cc_by_sa = ['docs/license_files/cc-by-sa-4.0']

for (key,source_params) in config_dict_cc_by.items():
    if 'license' in source_params:
        license_params = source_params['license']
        if 'file' in license_params:
            path = license_params['file']
            if path not in all_license_files_cc_by:
                all_license_files_cc_by.append(path)
print(all_license_files_cc_by)

for (key,source_params) in config_dict_cc_by_sa.items():
    if 'license' in source_params:
        license_params = source_params['license']
        if 'file' in license_params:
            path = license_params['file']
            if path not in all_license_files_cc_by_sa:
                all_license_files_cc_by_sa.append(path)
print(all_license_files_cc_by_sa)

def get_source_text(markdown_file):
    with open(markdown_file) as f:
        markdown_string = f.read()

    source_text = markdown_string \
                    .replace('*', '') \
                    .replace('<br>', '\n') \
                    .replace('#### ', '') \
                    .replace('[link]', '').replace('((', '(').replace('))', ')')

    return source_text

source_cc_by = get_source_text(os.path.join(ROOT_DIR, 'docs/sources_cc_by.md'))
source_cc_by_sa = get_source_text(os.path.join(ROOT_DIR, 'docs/sources_cc_by_sa.md'))

with open(EXPORT_PATH_CC_BY_LICENSE, 'w') as outfile:
    outfile.write(cc_by_header)
    outfile.write(source_cc_by)
    outfile.write('=======================================================================\n')
    outfile.write(complete_texts)
    for fname in all_license_files_cc_by:
        with open(os.path.join(ROOT_DIR, fname)) as infile:
            outfile.write(infile.read())
            outfile.write('\n')
            outfile.write('=======================================================================')
            outfile.write('\n')

with open(EXPORT_PATH_CC_BY_SA_LICENSE, 'w') as outfile:
    outfile.write(cc_by_sa_header)
    outfile.write(source_cc_by_sa)
    outfile.write('=======================================================================\n')
    outfile.write(complete_texts)
    for fname in all_license_files_cc_by_sa:
        with open(os.path.join(ROOT_DIR, fname)) as infile:
            outfile.write(infile.read())
            outfile.write('\n')
            outfile.write('=======================================================================')
            outfile.write('\n')
