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

import datetime
import logging
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

_resources = dict(
    about_md='docs/about.md',
    debug_dir='src/views/debug',
    downloaded_dir='data/inputs/downloaded',
    export_cc_by_csv='data/exports/cc_by/aggregated_cc_by.csv',
    export_cc_by_license='data/exports/cc_by/LICENSE',
    export_cc_by_nc_csv='data/exports/cc_by_nc/aggregated_cc_by_nc.csv',
    export_cc_by_nc_license='data/exports/cc_by_nc/LICENSE',
    export_cc_by_sa_csv='data/exports/cc_by_sa/aggregated_cc_by_sa.csv',
    export_cc_by_sa_license='data/exports/cc_by_sa/LICENSE',
    export_dir='data/exports',
    export_google_tos='data/exports/google_tos',
    export_google_tos_csv='data/exports/google_tos/aggregated_google_tos.csv',
    export_google_tos_license='data/exports/google_tos/LICENSE',
    export_search='data/exports/search_trends_symptoms_dataset',
    export_mobility='data/exports/google_mobility_reports/Regions',
    inputs_dir='data/inputs',
    locations_csv='data/exports/locations/locations.csv',
    locations_export_dir='data/exports/locations',
    locations_input_dir='data/inputs/static/locations/raw',
    locations_intermediate_dir='data/inputs/static/locations/intermediate',
    main_dir='src/views/main',
    readme_md='README.md',
    schema_yaml='src/config/schema.yaml',
    scraped_dir='data/inputs/scraped',
    sources_dir='src/config/sources',
    sources_md='docs/sources.md',
    sources_cc_by_md='docs/sources_cc_by.md',
    sources_cc_by_nc_md='docs/sources_cc_by_nc.md',
    sources_cc_by_sa_md='docs/sources_cc_by_sa.md',
    sources_google_tos_md='docs/sources_google_tos.md',
    spreadsheets_dir='data/inputs/scraped/spreadsheets',
    utils_dir='src/views/utils',
)

def path_to(resource_name):
    if resource_name not in _resources:
        raise ValueError(
            '"%s" is an unknown resource. Available resources are: %s' % (resource_name, _resources.keys()))
    return os.path.join(root_dir, _resources[resource_name])

def fetch_method_to_path_string(fetch_method):
    lookup_dict = {
        'AUTOMATIC_DOWNLOAD': 'downloaded',
        'MANUAL_DOWNLOAD': 'downloaded',
        'SCRAPED': 'scraped',
        'STATIC': 'static'
    }
    return lookup_dict[fetch_method]

def get_data_directory_path(params):
    source_key = params['config_key']
    fetch_method = params['fetch']['method']
    fetch_string = fetch_method_to_path_string(fetch_method)
    data_dir = os.path.join(path_to('inputs_dir'), fetch_string, source_key)
    file_name = params['fetch']['file']
    return data_dir, file_name

def has_data_from_date(params, date):
    path_to_data = path_to_data_for_date(params, date)
    path_dir = path_to_data['dir']
    path_file = path_to_data['file']
    return os.path.exists(os.path.join(path_dir, path_file))

def path_to_data_for_date(params, date):
    directory_path, file_name = get_data_directory_path(params)
    return {'dir': os.path.join(directory_path, date), 'file': file_name}

def all_data_most_to_least_recent(params):
    directory_path, file_name = get_data_directory_path(params)
    return all_subdirs_most_to_least_recent(directory_path, file_name)

def all_subdirs_most_to_least_recent(directory_path, file_name):
    try:
        _, subdirs, _ = next(os.walk(directory_path))
    except StopIteration:
        logging.warning('No subdirectories found for directory_path %s: skipping.', directory_path)
        subdirs = []
    subdirs_that_are_dates = []
    for sd in subdirs:
        try:
            sd_date = datetime.datetime.strptime(sd, '%Y-%m-%d').date()
            subdirs_that_are_dates.append(sd_date)
        except ValueError:
            continue
    # Sorted most recent to least recent
    sorted_subdir_dates = sorted(subdirs_that_are_dates, reverse=True)
    sorted_subdir_paths_with_data = []
    # Iterate from most recent to least recent, if you find
    # a subdir containing the correct filename then append to return value
    for subdir_date in sorted_subdir_dates:
        date_str = subdir_date.strftime('%Y-%m-%d')
        path_to_file = os.path.join(directory_path, date_str, file_name)
        if os.path.exists(path_to_file) or file_name is None:
            subdir_dict = {'path': path_to_file, 'date': subdir_date}
            sorted_subdir_paths_with_data.append(subdir_dict)
    # If you never found a subdir with this file, will return an empty list
    return sorted_subdir_paths_with_data

def most_recent_subdir(directory_path, file_name):
    sorted_subdir_list = all_subdirs_most_to_least_recent(directory_path, file_name)
    if len(sorted_subdir_list) > 0:
        return sorted_subdir_list[0]
    else:
        return {'path': None, 'date': None}

# Returns a dictionary with 'path' and 'date', which are None if no data exists
def most_recent_data(params):
    sorted_data_paths = all_data_most_to_least_recent(params)
    if len(sorted_data_paths) > 0:
        return sorted_data_paths[0]
    else:
        return {'path': None, 'date': None}
