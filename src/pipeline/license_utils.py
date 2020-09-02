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
import path_utils
import re

def get_license_files(config_dict, required_licenses=None):
    if required_licenses is None:
        license_files = []
    else:
        license_files = required_licenses
    source_license_files = [source['license']['file'] for source in config_dict.values()
                            if 'license' in source and 'file' in source['license']]
    license_files = sorted(set(license_files + source_license_files))
    return license_files

def markdown_to_plaintext(markdown_file):
    with open(markdown_file) as f:
        markdown_string = f.read()

    # pylint: disable=bad-continuation
    source_text = (markdown_string.replace('*', '')
                                  .replace('<br>', '\n')
                                  .replace('#### ', '')
                                  .replace('[link]', '')
                                  .replace('((', '(')
                                  .replace('))', ')'))

    # Replace markdown links "[text](link)" with "text at <link>"
    name_regex = '[^]]+'
    url_regex = 'http[s]?://[^)]+'  # http:// or https:// followed by anything but a closing paren
    markup_regex = r'\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)
    source_text = re.sub(markup_regex, lambda x: f'{x[1]} at {x[2]}', source_text)

    return source_text

def text_output(path):
    textwrapper = textwrap.TextWrapper(width=100, replace_whitespace=False,
                                       break_long_words=False, break_on_hyphens=False)
    source_text = markdown_to_plaintext(path)
    split_text = str.splitlines(source_text)
    filled_text = [textwrapper.fill(t) for t in split_text]
    return filled_text

def export_aggregated_license(export_path, sources_path, license_files, header, include_license_texts=True):
    complete_texts = '''Complete license texts for each unique license are available below:\n\n'''
    with open(export_path, 'w') as outfile:
        outfile.write(header)
        for line in text_output(sources_path):
            if 'Last accessed:' not in line:
                outfile.write(line)
                outfile.write('\n')
        if include_license_texts:
            outfile.write('=======================================================================\n')
            outfile.write(complete_texts)
            for fname in license_files:
                with open(os.path.join(path_utils.root_dir, fname)) as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')
                    outfile.write('=======================================================================')
                    outfile.write('\n')
