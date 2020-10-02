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

# pylint: disable=no-value-for-parameter

import streamlit as st
import sys
import os

PIPELINE_DIR = os.path.join(os.path.dirname(__file__), '../../', 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import path_utils

sys.path.append(path_utils.path_to('main_dir'))
sys.path.append(path_utils.path_to('utils_dir'))

import pipeline_explorer

st.sidebar.markdown('# Select view:')
radio_selection = st.sidebar.radio('', ['Pipeline Explorer'])
st.sidebar.markdown('---')

if radio_selection == 'Pipeline Explorer':
    pipeline_explorer.pipeline()
