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

import yamale
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')
SOURCE_DIR = os.path.join(ROOT_DIR, 'src/config/sources')

def test_config_file_schema():
     schema = yamale.make_schema(os.path.join(ROOT_DIR, 'src/config/schema.yaml'))
     source_files = os.listdir(SOURCE_DIR)
     for source_file in source_files:
         print(source_file)
         data = yamale.make_data(os.path.join(SOURCE_DIR, source_file))
         yamale.validate(schema, data, strict=True)
