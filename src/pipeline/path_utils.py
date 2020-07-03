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


CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))

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
    data_dir = os.path.join(ROOT_DIR, 'data/inputs', fetch_string, source_key)
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
        if os.path.exists(path_to_file):
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
