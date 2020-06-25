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

import textwrap
import os
from path_utils import ROOT_DIR

def get_license_files(config_dict, required_licenses=None):
    if required_licenses is None:
        license_files = []
    else:
        license_files = required_licenses
    for source_params in config_dict.values():
        if 'license' in source_params:
            license_params = source_params['license']
            if 'file' in license_params:
                path = license_params['file']
                if path not in license_files:
                    license_files.append(path)
    return license_files

def markdown_to_plaintext(markdown_file):
    with open(markdown_file) as f:
        markdown_string = f.read()

    source_text = markdown_string \
                    .replace('*', '') \
                    .replace('<br>', '\n') \
                    .replace('#### ', '') \
                    .replace('[link]', '').replace('((', '(').replace('))', ')')

    return source_text

def text_output(path):
    textwrapper = textwrap.TextWrapper(width=100, replace_whitespace=False,
                                       break_long_words=False, break_on_hyphens=False)
    source_text = markdown_to_plaintext(path)
    split_text = str.splitlines(source_text)
    filled_text = [textwrapper.fill(t) for t in split_text]
    return filled_text

def export_aggregated_license(export_path, sources_path, license_files, header):
    complete_texts = '''Complete license texts for each unique license are available below:\n\n'''
    with open(export_path, 'w') as outfile:
        outfile.write(header)
        for line in text_output(sources_path):
            outfile.write(line)
            outfile.write('\n')
        outfile.write('=======================================================================\n')
        outfile.write(complete_texts)
        for fname in license_files:
            with open(os.path.join(ROOT_DIR, fname)) as infile:
                outfile.write(infile.read())
                outfile.write('\n')
                outfile.write('=======================================================================')
                outfile.write('\n')
