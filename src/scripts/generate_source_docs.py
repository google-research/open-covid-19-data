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
SOURCES_PATH = os.path.join(ROOT_DIR, 'docs/sources.md')
YAML_PATH = os.path.join(ROOT_DIR, 'src/config/docs.yaml')

todays_date = datetime.today().strftime('%Y-%m-%d')

with open(YAML_PATH) as file:
    sources = yaml.load(file, Loader=yaml.FullLoader)

def source_and_link_str(source_name, link):
    str = source_name
    str += ' ([link]('
    str += link
    str += '))'
    return str

with open(SOURCES_PATH, 'w') as out:
    for source in sources.values():
        out.write('#### ' + source['country'] + '\n')
        if 'source_name' in source:
            out.write('**Source name:** ')
            out.write(source_and_link_str(source['source_name'], source['main_link']))
            out.write('<br>')
        if 'data_link' in source:
            out.write('**Link to data:** ')
            out.write(source['data_link'])
            out.write('<br>')
        if 'original' in source:
            original_source = source['original']
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
        if 'aggregated_by' in source:
            agg_source = source['aggregated_by']
            out.write('**Data aggregated by:** ')
            out.write(source_and_link_str(agg_source['source_name'], agg_source['main_link']))
            out.write('<br>')
            if 'license'in agg_source:
                out.write('**License for aggregated data:** ')
                out.write(source_and_link_str(agg_source['license']['name'], agg_source['license']['link']))
                out.write('<br>')
        if 'attribution' in source:
            out.write('**Attribution:** ')
            out.write(source['attribution'])
            out.write('<br>')
        if 'description' in source:
            out.write('**Description:** ')
            out.write(source['description'])
            out.write('<br>')
        if 'license' in source:
            out.write('**License:** ')
            out.write(source_and_link_str(source['license']['name'], source['license']['link']))
            out.write('<br>')

        out.write('**Last accessed:** ' + todays_date)
        out.write('\n\n')
