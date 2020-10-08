# Copyright 2020 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import argparse
import sys
import re

PIPELINE_DIR = os.path.join(os.path.dirname(__file__), '../../', 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import export_utils

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', required=True)
parser.add_argument('--output_dir', required=True)
parser.add_argument('--historical', action='store_true')

args = parser.parse_args()

country_code_to_dir_name = {'US': 'United States of America'}
HISTORICAL_YEAR_LIST = ['2017', '2018', '2019']
CURRENT_YEAR_LIST = ['2020']

class DestinationDict():
    """
        A class where self.dest_dict is a dictionary where each item corresponds
        to one destination directory. The key is (year, country_code, state) because
        this tuple uniquely determines the destination directory.
        The value is a dictionary with the following format:
            { 'dest_dir': the destination directory,
              'source_file_objs': a list of SearchFileObjects
              'historical': a boolean, whether these files are historical or not
            }
    """
    def __init__(self):
        self.dest_dict = {}

    def add_source_file(self, search_file_obj):
        year = search_file_obj.year
        historical = year in HISTORICAL_YEAR_LIST
        country_code = search_file_obj.country_code
        state = search_file_obj.state
        key_tuple = (year, country_code, state)
        if key_tuple in self.dest_dict:
            self.dest_dict[key_tuple]['source_file_objs'].append(search_file_obj)
        else:
            dest_dir = self.get_destination_dir(search_file_obj)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            if not historical:
                self.write_readme(dest_dir, year, country_code, state)
            self.dest_dict[key_tuple] = {
                'dest_dir': dest_dir,
                'historical': historical,
                'source_file_objs': [search_file_obj]
            }

    def get_destination_dir(self, search_file_obj):
        if search_file_obj.state is None:  # country level
            if search_file_obj.year in HISTORICAL_YEAR_LIST:
                dest_dir = os.path.join('historical', f'{search_file_obj.country_code}_search_trends_symptoms_dataset')
            else:
                dest_dir = country_code_to_dir_name[search_file_obj.country_code]
        else:  # state level
            if search_file_obj.year in HISTORICAL_YEAR_LIST:
                dest_dir = os.path.join('historical',
                                        'US_' + search_file_obj.get_state(sep='_') + '_search_trends_symptoms_dataset')
            else:
                subregions_dir = os.path.join(country_code_to_dir_name[search_file_obj.country_code], 'subregions')
                dest_dir = os.path.join(subregions_dir, search_file_obj.get_state(sep=' '))

        dest_dir = os.path.join(args.output_dir, dest_dir)
        return dest_dir

    # inputs=True for the README that goes in data/inputs, inputs=False for the README that goes in data/exports
    def get_readme_text(self, year, country_code, state, inputs=True):
        region_prefix = f'{country_code}' if state is None else f'{country_code}_{state}'  # example: US_West_Virginia
        daily_filename = f'{year}_{region_prefix}_daily_symptoms_dataset.csv'
        weekly_filename = f'{year}_{region_prefix}_weekly_symptoms_dataset.csv'

        if inputs:
            # Link to the README at data/inputs/downloaded/search_trends_symptoms_dataset
            dataset_doc_link = '../../README.md' if state is None else '../../../../README.md'
        else:
            # To link to the README at data/exports/search_trends_symptoms_dataset, you need one less level
            dataset_doc_link = '../README.md' if state is None else '../../../README.md'

        # pylint: disable=inconsistent-quotes,line-too-long
        readme_string = (f"### Terms of use\n"
                         f"To download or use the data, you must agree to the Google [Terms of Service](https://policies.google.com/terms).\n\n"
                         f"### Accessing this region's CSV files\n"
                         f"The CSV files for the **current year** can be found here:\n"
                         f"- CSV for symptoms provided at a daily resolution: [{daily_filename}]({daily_filename})\n"
                         f"- CSV for symptoms provided at a weekly resolution: [{weekly_filename}]({weekly_filename})\n\n"
                         f"CSV files for **previous years** (both daily and weekly), are available in the release assets of this repository and can be downloaded as a zip file: [{region_prefix}_search_trends_symptoms_dataset.zip](https://github.com/google-research/open-covid-19-data/releases/download/v0.0.2/{region_prefix}_search_trends_symptoms_dataset.zip)\n\n"
                         f"To learn more about the dataset, how we generate it and preserve privacy, read the [dataset documentation]({dataset_doc_link}).")
        # pylint: enable=inconsistent-quotes,line-too-long
        return readme_string

    def move_all_source_files_to_dest(self):
        for key in self.dest_dict:
            source_file_objs = self.dest_dict[key]['source_file_objs']
            dest_dir = self.dest_dict[key]['dest_dir']
            for source_file_obj in source_file_objs:
                shutil.copy(source_file_obj.source_path, dest_dir)

    # This is to create release assets for historical files
    def add_region_codes_and_zip_historical_files(self):
        for key in self.dest_dict:
            if self.dest_dict[key]['historical']:
                dest_dir = self.dest_dict[key]['dest_dir']
                historical_dir = os.path.join(args.output_dir, 'historical')
                for dest_filename in os.listdir(dest_dir):
                    if dest_filename.endswith('.csv'):
                        dest_file = os.path.join(dest_dir, dest_filename)
                        export_utils.write_csv_with_open_covid_region_code_added(dest_file, dest_file)
                dir_name = os.path.basename(dest_dir)
                shutil.make_archive(
                    base_name=os.path.join(historical_dir, 'zipped', dir_name),
                    format='zip', base_dir=os.path.basename(dest_dir), root_dir=historical_dir)

    def write_readme(self, dest_dir, year, country_code, state):
        readme_text = self.get_readme_text(year, country_code, state)
        with open(os.path.join(dest_dir, 'README.md'), 'w') as f:
            f.write(readme_text)

class SearchFileObject():
    """ An object that uses a regex to extract information from the search data filename
        and store it as fields.
        Fields:
            source_path: the full path to the search data file
            source_filename: the basename of the file
            year: four-digit year
            country_code: a two-letter code for the country
            state: underscore-separated string for the state. None if country-level.
            region_level: 'country' or 'state'
            time_granularity: 'daily' or 'weekly'
    """
    def __init__(self, source_dir_path, source_filename):
        self.source_path = os.path.join(source_dir_path, source_filename)
        self.source_filename = source_filename
        filename_regex = r'^(\d{4})_([a-zA-Z]{2})(_([a-zA-Z_]*))?_(daily|weekly)_symptoms_dataset.csv$'
        m = re.match(filename_regex, self.source_filename)
        self.year = m.group(1)
        self.country_code = m.group(2)
        self.state = m.group(4)
        if self.state is None:
            self.region_level = 'country'
        else:
            self.region_level = 'state'
        self.time_granularity = m.group(5)  # 'daily' or 'weekly'

    def __repr__(self):
        return self.source_path

    def get_state(self, sep='_'):
        if self.state is None:
            return ''
        else:
            state_word_list = self.state.split('_')
            return sep.join(state_word_list)

dest_dict = DestinationDict()
for dir_path, subdirs, files in os.walk(args.input_dir):
    for file in files:
        filename = os.path.basename(file)
        if filename.endswith('csv'):
            search_data_file = SearchFileObject(dir_path, file)
            dest_dict.add_source_file(search_data_file)

dest_dict.move_all_source_files_to_dest()
dest_dict.add_region_codes_and_zip_historical_files()
