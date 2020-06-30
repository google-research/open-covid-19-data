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

# pylint: disable=no-value-for-parameter

import streamlit as st
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')
DEBUG_DIR = os.path.join(ROOT_DIR, 'src/views/debug')

sys.path.append(PIPELINE_DIR)
sys.path.append(DEBUG_DIR)

import load_all_sources

st.sidebar.markdown('# Select debug view:')
radio_selection = st.sidebar.radio('', ['Load all sources'])
st.sidebar.markdown('---')

if radio_selection == 'Load all sources':
    load_all_sources.load_all_data_sources()
