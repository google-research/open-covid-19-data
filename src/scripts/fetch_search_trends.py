import os
import shutil
import argparse
import sys

PIPELINE_DIR = os.path.join(os.path.dirname(__file__), '../../', 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import export_utils

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', required=True)
parser.add_argument('--output_dir', required=True)
parser.add_argument('--historical', action='store_true')

args = parser.parse_args()

# Example region_prefix = US_West_Virginia
def get_readme_text(region_prefix, us_level=False):
    daily_filename = f'2020_{region_prefix}_daily_symptoms_dataset.csv'
    weekly_filename = f'2020_{region_prefix}_weekly_symptoms_dataset.csv'

    # Link to the README at data/inputs/downloaded/search_trends_symptoms_dataset
    dataset_doc_link = '../../README.md' if us_level else '../../../../README.md'
    # To link to the README at data/exports/search_trends_symptoms_dataset, you need one less level
    # dataset_doc_link = '../README.md' if us_level else '../../../README.md'

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

# There will always be two underscores before the state name, and three underscores after.
# This returns the state name with underscores between words, i.e West_Virginia
def get_state_underscore_sep_from_filename(input_filename):
    split_string = input_filename.split('_')
    state_word_list = split_string[2:-3]
    state_underscore_sep = '_'.join(state_word_list)
    return state_underscore_sep

if args.historical:
    print('historical')
    years = ['2017', '2018', '2019']
else:
    print('not historical')
    years = ['2020']

us_path = os.path.join(args.input_dir, 'US', 'states')
states_path = os.path.join(args.input_dir, 'US', 'counties')
us_files = []
state_files = []

for path, subdirs, files in os.walk(us_path):
    for file in files:
        filename = os.path.basename(file)
        if filename.endswith('csv') and filename.split('_')[0] in years:
            us_files.append(os.path.join(path, file))

for path, subdirs, files in os.walk(states_path):
    for file in files:
        filename = os.path.basename(file)
        if filename.endswith('csv') and filename.split('_')[0] in years:
            state_files.append(os.path.join(path, file))

# 50 states + 1 country = 51 locations x 4 years (2017, 2018, 2019, 2020) x 2 files per year (daily, weekly) = 408 files
if args.historical:
    assert len(us_files) == 6
    assert len(state_files) == 300
else:
    assert len(us_files) == 2
    assert len(state_files) == 100

list_of_states = sorted(list({get_state_underscore_sep_from_filename(f) for f in state_files}))
print('list of states: ', list_of_states)
assert len(list_of_states) == 50

us_dir_name = 'US_search_trends_symptoms_dataset' if args.historical else 'United States of America'
us_dir = os.path.join(args.output_dir, us_dir_name)
os.makedirs(us_dir)
for file in us_files:
    filename = os.path.basename(file)
    shutil.copyfile(file, os.path.join(us_dir, filename))
    if not args.historical:
        with open(os.path.join(us_dir, 'README.md'), 'w') as f:
            f.write(get_readme_text('US', us_level=True))

if not args.historical:
    subregions_dir = os.path.join(us_dir, 'subregions')
    os.makedirs(subregions_dir)

for state in list_of_states:
    print('state: ', state)
    this_states_files = list(filter(lambda f, s=state: get_state_underscore_sep_from_filename(f) == s, state_files))
    print('this_states_files: ', this_states_files)
    # Release assets have to be flat, so states are *not* nested under US directory
    if args.historical:
        assert len(this_states_files) == 6
        this_states_dir = os.path.join(args.output_dir, 'US_' + state + '_search_trends_symptoms_dataset')
    # File structure in the repo allows for nesting, so states *are* nested under US/subregions directory
    else:
        assert len(this_states_files) == 2
        state_space_sep = state.replace('_', ' ')
        this_states_dir = os.path.join(subregions_dir, state_space_sep)
    os.makedirs(this_states_dir)
    # In the repo, add a README for each location that links to the files and release assets
    if not args.historical:
        with open(os.path.join(this_states_dir, 'README.md'), 'w') as f:
            f.write(get_readme_text('US_' + state))
    for file in this_states_files:
        filename = os.path.basename(file)
        shutil.copyfile(file, os.path.join(this_states_dir, filename))

# # For historical data: add region_code column to every file, then zip each folder
if args.historical:
    all_release_asset_files = []
    for path, subdirs, files in os.walk(args.output_dir):
        for file in files:
            if os.path.basename(file).endswith('csv'):
                all_release_asset_files.append(os.path.join(path, file))

    for file in all_release_asset_files:
        export_utils.write_csv_with_open_covid_region_code_added(file, file)

    # Zip each folder
    count = 0
    for dir_name in os.listdir(args.output_dir):
        if dir_name != '.DS_Store':
            shutil.make_archive(
                base_name=os.path.join(args.output_dir, 'zipped', dir_name),
                format='zip', base_dir=dir_name, root_dir=args.output_dir)
            count += 1
    print('count: ', count)
    assert count == 51
