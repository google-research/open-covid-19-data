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

import yamale
import os
import sys

PIPELINE_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')), 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import path_utils


def test_config_file_schema():
     schema = yamale.make_schema(path_utils.path_to('schema_yaml'))
     source_files = os.listdir(path_utils.path_to('sources_dir'))
     for source_file in source_files:
         print(source_file)
         data = yamale.make_data(os.path.join(path_utils.path_to('sources_dir'), source_file))
         yamale.validate(schema, data, strict=True)
