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

from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
SOURCES_PATH_ALL = os.path.join(ROOT_DIR, 'docs/sources.md')
SOURCES_PATH_CC_BY = os.path.join(ROOT_DIR, 'docs/sources_cc_by.md')
SOURCES_PATH_CC_BY_SA = os.path.join(ROOT_DIR, 'docs/sources_cc_by_sa.md')
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import config
import path_utils

# README should contain all sources in the repo (sources_all)
# sources_cc_by creates aggregated license for cc_by, should contain non-cc-by-sa sources, including google_tos
# sources_cc_by_sa creates aggregated license for cc_by_sa, should contain cc-by-sa sources, but no google_tos
sources_all = config.read_config(filter_no_load_func=False, cc_by_sa=True, google_tos=True)
alphabetized_sources_all = sorted(sources_all.items(), key = lambda x: x[1]['attribution']['title'])
sources_cc_by = config.read_config(filter_no_load_func=True, cc_by_sa=False, google_tos=True)
alphabetized_sources_cc_by = sorted(sources_cc_by.items(), key = lambda x: x[1]['attribution']['title'])
sources_cc_by_sa = config.read_config(filter_no_load_func=True, cc_by_sa=True, google_tos=False)
alphabetized_sources_cc_by_sa = sorted(sources_cc_by_sa.items(), key = lambda x: x[1]['attribution']['title'])

def source_and_link_str(source_name, link):
    str = source_name
    str += ' ([link]('
    str += link
    str += '))'
    return str

def add_last_accessed_date(source):
    try:
        most_recent_date = path_utils.most_recent_data(source)['date']
        source['last_accessed'] = str(most_recent_date)
        return source
    except:
        return source

def write_source(item, out):
    source = item[1]
    source = add_last_accessed_date(source)
    attribution = source['attribution']
    out.write('#### ' + attribution['title'] + '\n')
    if 'source_name' in attribution:
        out.write('**Source name:** ')
        if 'main_link' in attribution:
            out.write(source_and_link_str(attribution['source_name'], attribution['main_link']))
        else:
            out.write(attribution['source_name'])
        out.write('<br>')
    if 'data_link' in attribution:
        out.write('**Link to data:** ')
        out.write(attribution['data_link'])
        out.write('<br>')
    if 'help_center' in attribution:
        out.write('**Help Center:** ')
        out.write(attribution['help_center'])
        out.write('<br>')
    if 'copyright_notice' in attribution:
        out.write('**Copyright notice:** ')
        out.write(attribution['copyright_notice'])
        out.write('<br>')
    if 'original' in attribution:
        original_source = attribution['original']
        out.write('**Original data source:** ')
        out.write(source_and_link_str(original_source['source_name'], original_source['main_link']))
        out.write('<br>')
        if 'data_link' in original_source:
            out.write('**Link to original data:** ')
            out.write(original_source['data_link'])
            out.write('<br>')
        if 'license'in original_source:
            out.write('**License for original data:** ')
            out.write(source_and_link_str(original_source['license']['name'], original_source['license']['link']))
            out.write('<br>')
    if 'aggregated_by' in attribution:
        agg_source = attribution['aggregated_by']
        out.write('**Data aggregated by:** ')
        out.write(source_and_link_str(agg_source['source_name'], agg_source['main_link']))
        out.write('<br>')
        if 'license'in agg_source:
            out.write('**License for aggregated data:** ')
            out.write(source_and_link_str(agg_source['license']['name'], agg_source['license']['link']))
            out.write('<br>')
    if 'description' in attribution:
        out.write('**Description:** ')
        out.write(attribution['description'])
        out.write('<br>')
    if 'documentation' in attribution:
        out.write('**Documentation:** ')
        out.write(attribution['documentation'])
        out.write('<br>')
    if 'terms' in attribution:
        out.write('**Terms:** ')
        out.write(attribution['terms'])
        out.write('<br>')
    if 'license' in source:
        out.write('**License:** ')
        out.write(source_and_link_str(source['license']['name'], source['license']['link']))
        out.write('<br>')
    if 'citation' in attribution:
        out.write('**Citation:**')
        out.write('\n```\n')
        out.write(attribution['citation'])
        out.write('\n```\n')
        #out.write('<br>')
    if 'last_accessed' in source:
        out.write('**Last accessed:** ' + source['last_accessed'])
    out.write('\n\n')

with open(SOURCES_PATH_ALL, 'w') as out:
    for item in alphabetized_sources_all:
        write_source(item, out)

with open(SOURCES_PATH_CC_BY, 'w') as out:
    for item in alphabetized_sources_cc_by:
        write_source(item, out)

with open(SOURCES_PATH_CC_BY_SA, 'w') as out:
    for item in alphabetized_sources_cc_by_sa:
        write_source(item, out)
