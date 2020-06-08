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

ABOUT_PATH = os.path.join(ROOT_DIR, 'docs/about.md')
SOURCES_PATH = os.path.join(ROOT_DIR, 'docs/sources_cc_by_sa.md')
README_PATH = os.path.join(ROOT_DIR, 'README.md')

with open(README_PATH, 'w') as outfile:
    with open(ABOUT_PATH, 'r') as infile:
        outfile.write(infile.read())

    outfile.write('\n\n## Data Sources\n')
    with open(SOURCES_PATH, 'r') as infile:
        outfile.write(infile.read())
