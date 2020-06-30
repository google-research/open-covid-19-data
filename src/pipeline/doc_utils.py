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

import path_utils


def source_and_link_str(source_name, link):
    result = source_name
    result += ' ([link]('
    result += link
    result += '))'
    return result

def add_last_accessed_date(source):
    try:
        most_recent_date = path_utils.most_recent_data(source)['date']
        source['last_accessed'] = str(most_recent_date)
        return source
    except KeyError:
        return source

def write_single_source(item, out):
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
    if 'license' in source and 'name' in source['license']:
        out.write('**License:** ')
        out.write(source_and_link_str(source['license']['name'], source['license']['link']))
        out.write('<br>')
    if 'citation' in attribution:
        out.write('**Citation:**')
        out.write('\n```\n')
        out.write(attribution['citation'])
        out.write('\n```\n')
    if 'last_accessed' in source:
        out.write('**Last accessed:** ' + source['last_accessed'])
    out.write('\n\n')

def write_sources(source_list, source_path):
    alphabetized_source_list = sorted(source_list.items(), key=lambda x: x[1]['attribution']['title'])
    with open(source_path, 'w') as out:
        for item in alphabetized_source_list:
            write_single_source(item, out)
