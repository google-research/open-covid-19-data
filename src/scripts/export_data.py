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
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import args_utils
import license_utils
import export_utils
import doc_utils
import config


args = args_utils.get_parser().parse_args()

if not args.whitelist:
    logging.warning('RUNNING WITHOUT THE WHITELIST! DO NOT MAKE A PULL REQUEST WITH THE OUTPUT!')

# For Google TOS, this script only updates the exported data, but doesn't modify docs or licenses.
# The Google TOS license file in data/exports/sources_google_tos is a static file not an aggregated license.
EXPORT_PATH_CC_BY = os.path.join(ROOT_DIR, 'data/exports/cc_by/aggregated_cc_by.csv')
EXPORT_PATH_CC_BY_SA = os.path.join(ROOT_DIR, 'data/exports/cc_by_sa/aggregated_cc_by_sa.csv')
EXPORT_PATH_GOOGLE_TOS = os.path.join(ROOT_DIR, 'data/exports/google_tos/aggregated_google_tos.csv')

SOURCES_PATH_ALL = os.path.join(ROOT_DIR, 'docs/sources.md')
SOURCES_PATH_CC_BY = os.path.join(ROOT_DIR, 'docs/sources_cc_by.md')
SOURCES_PATH_CC_BY_SA = os.path.join(ROOT_DIR, 'docs/sources_cc_by_sa.md')

ABOUT_PATH = os.path.join(ROOT_DIR, 'docs/about.md')
README_PATH = os.path.join(ROOT_DIR, 'README.md')

EXPORT_PATH_CC_BY_LICENSE = os.path.join(ROOT_DIR, 'data/exports/cc_by/LICENSE')
EXPORT_PATH_CC_BY_SA_LICENSE = os.path.join(ROOT_DIR, 'data/exports/cc_by_sa/LICENSE')

sources_all = config.read_config(
    cc_by=True, cc_by_sa=True, google_tos=True, filter_not_approved=args.whitelist)
sources_cc_by = config.read_config(
    cc_by=True, cc_by_sa=False, google_tos=False, filter_not_approved=args.whitelist)
sources_cc_by_sa = config.read_config(
    cc_by=True, cc_by_sa=True, google_tos=False, filter_not_approved=args.whitelist)
sources_google_tos = config.read_config(
    cc_by=False, cc_by_sa=False, google_tos=True, filter_not_approved=args.whitelist)

# Step 1: Write source docs

# SOURCES_PATH_ALL contains every source, used to create the README.
doc_utils.write_sources(sources_all, SOURCES_PATH_ALL)
# SOURCES_PATH_CC_BY used to create aggregated license for cc-by.
doc_utils.write_sources(sources_cc_by, SOURCES_PATH_CC_BY)
# SOURCES_PATH_CC_BY_SA used to create aggregated license for cc-by-sa.
doc_utils.write_sources(sources_cc_by_sa, SOURCES_PATH_CC_BY_SA)

# Step 2: Write the README (needs to happen after writing the source docs)

with open(README_PATH, 'w') as outfile:
    with open(ABOUT_PATH, 'r') as infile:
        outfile.write(infile.read())

    outfile.write('\n\n## Data Sources\n')
    with open(SOURCES_PATH_ALL, 'r') as infile:
        outfile.write(infile.read())

# Step 3: Export aggregated license files

cc_by_header = ('''The file `aggregated_cc_by.csv` is licensed under Creative Commons Attribution'''
                ''' 4.0 International.\n\nIt includes content under the following licenses:\n\n''')

cc_by_sa_header = ('''The file `aggregated_cc_by_sa.csv` is licensed under Creative Commons Attribution-ShareAlike'''
                   ''' 4.0 International.\n\nIt includes content under the following licenses:\n\n''')

all_license_files_cc_by = license_utils.get_license_files(sources_cc_by,
                                                          required_licenses=['docs/license_files/cc-by-4.0'])
all_license_files_cc_by_sa = license_utils.get_license_files(sources_cc_by_sa,
                                                             required_licenses=['docs/license_files/cc-by-sa-4.0'])

license_utils.export_aggregated_license(EXPORT_PATH_CC_BY_LICENSE, SOURCES_PATH_CC_BY,
                                        all_license_files_cc_by, cc_by_header)
license_utils.export_aggregated_license(EXPORT_PATH_CC_BY_SA_LICENSE, SOURCES_PATH_CC_BY_SA,
                                        all_license_files_cc_by_sa, cc_by_sa_header)

# Step 4: Export aggregated data files

export_utils.export_data(config_dict=sources_cc_by, export_path=EXPORT_PATH_CC_BY)
print('Done exporting cc by data.')

export_utils.export_data(config_dict=sources_cc_by_sa, export_path=EXPORT_PATH_CC_BY_SA)
print('Done exporting cc by-sa data.')

export_utils.export_data(config_dict=sources_google_tos, export_path=EXPORT_PATH_GOOGLE_TOS)
print('Done exporting Google TOS data.')
