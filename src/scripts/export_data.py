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

PIPELINE_DIR = os.path.join(os.path.dirname(__file__), '../../', 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import args_utils
import license_utils
import export_utils
import doc_utils
import config
import path_utils


args = args_utils.get_parser().parse_args()
path_utils.root_dir = args.publish_dir

if not args.allowlist:
    logging.warning('RUNNING WITHOUT THE ALLOWLIST! DO NOT MAKE A PULL REQUEST WITH THE OUTPUT!')

sources_all = config.read_config(
    cc_by=True, cc_by_sa=True, cc_by_nc=True, google_tos=True, filter_not_approved=args.allowlist)
sources_cc_by = config.read_config(
    cc_by=True, cc_by_sa=False, cc_by_nc=False, google_tos=False, filter_not_approved=args.allowlist)
sources_cc_by_sa = config.read_config(
    cc_by=True, cc_by_sa=True, cc_by_nc=False, google_tos=False, filter_not_approved=args.allowlist)
sources_cc_by_nc = config.read_config(
    cc_by=True, cc_by_sa=False, cc_by_nc=True, google_tos=False, filter_not_approved=args.allowlist)
sources_google_tos = config.read_config(
    cc_by=False, cc_by_sa=False, cc_by_nc=False, google_tos=True, filter_not_approved=args.allowlist)
google_search_source = {'search_trends_symptoms_dataset': sources_google_tos['search_trends_symptoms_dataset']}
del sources_google_tos['search_trends_symptoms_dataset']
print('sources google tos: ', sources_google_tos)
print('google_search_source:', google_search_source)

# Step 1: Write source docs

# sources_md contains every source, used to create the README.
doc_utils.write_sources(sources_all, path_utils.path_to('sources_md'))
# sources_cc_by_md is used to create aggregated license for cc-by.
doc_utils.write_sources(sources_cc_by, path_utils.path_to('sources_cc_by_md'))
# sources_cc_by_sa_md is used to create aggregated license for cc-by-sa.
doc_utils.write_sources(sources_cc_by_sa, path_utils.path_to('sources_cc_by_sa_md'))
# sources_cc_by_nc_md is used to create aggregated license for cc-by-nc.
doc_utils.write_sources(sources_cc_by_nc, path_utils.path_to('sources_cc_by_nc_md'))

# Step 2: Write the README (needs to happen after writing the source docs)

with open(path_utils.path_to('readme_md'), 'w') as outfile:
    with open(path_utils.path_to('about_md'), 'r') as infile:
        outfile.write(infile.read())

    outfile.write('\n\n## Data Sources\n')
    with open(path_utils.path_to('sources_md'), 'r') as infile:
        outfile.write(infile.read())

# Step 3: Export aggregated license files

cc_by_header = ('''The file `aggregated_cc_by.csv` is licensed under Creative Commons Attribution'''
                ''' 4.0 International.\n\nIt includes content under the following licenses:\n\n''')

cc_by_sa_header = ('''The file `aggregated_cc_by_sa.csv` is licensed under Creative Commons Attribution-ShareAlike'''
                   ''' 4.0 International.\n\nIt includes content under the following licenses:\n\n''')

cc_by_nc_header = ('''The file `aggregated_cc_by_nc.csv` is licensed under Creative Commons Attribution-NonCommercial'''
                   ''' 4.0 International.\n\nIt includes content under the following licenses:\n\n''')


all_license_files_cc_by = license_utils.get_license_files(sources_cc_by,
                                                          required_licenses=['docs/license_files/cc-by-4.0'])
all_license_files_cc_by_sa = license_utils.get_license_files(sources_cc_by_sa,
                                                             required_licenses=['docs/license_files/cc-by-sa-4.0'])
all_license_files_cc_by_nc = license_utils.get_license_files(sources_cc_by_nc,
                                                             required_licenses=[
                                                                 'docs/license_files/cc-by-nc-4.0',
                                                                 'docs/license_files/nytimes'])

license_utils.export_aggregated_license(path_utils.path_to('export_cc_by_license'),
                                        path_utils.path_to('sources_cc_by_md'),
                                        all_license_files_cc_by,
                                        cc_by_header)
license_utils.export_aggregated_license(path_utils.path_to('export_cc_by_sa_license'),
                                        path_utils.path_to('sources_cc_by_sa_md'),
                                        all_license_files_cc_by_sa,
                                        cc_by_sa_header)
license_utils.export_aggregated_license(path_utils.path_to('export_cc_by_nc_license'),
                                        path_utils.path_to('sources_cc_by_nc_md'),
                                        all_license_files_cc_by_nc,
                                        cc_by_nc_header)

# Step 4: Export aggregated data files

export_utils.export_data(config_dict=sources_cc_by, export_path=path_utils.path_to('export_cc_by_csv'))
print('Done exporting cc by data.')

export_utils.export_data(config_dict=sources_cc_by_sa, export_path=path_utils.path_to('export_cc_by_sa_csv'))
print('Done exporting cc by-sa data.')

export_utils.export_data(config_dict=sources_cc_by_nc, export_path=path_utils.path_to('export_cc_by_nc_csv'))
print('Done exporting cc by-nc data.')

export_utils.export_data(config_dict=sources_google_tos, export_path=path_utils.path_to('export_mobility'))
print('Done exporting Google Mobility data.')
export_utils.export_data(config_dict=google_search_source, export_path=path_utils.path_to('export_search'))
print('Done exporting Google Search data.')
