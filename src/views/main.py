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

import streamlit as st
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')
MAIN_DIR = os.path.join(ROOT_DIR, 'src/views/main')
UTILS_DIR = os.path.join(ROOT_DIR, 'src/views/utils')

sys.path.append(PIPELINE_DIR)
sys.path.append(MAIN_DIR)
sys.path.append(UTILS_DIR)

import pipeline_explorer
import plot_utils

st.sidebar.markdown("# Select view:")
radio_selection = st.sidebar.radio('', ['Pipeline Explorer'])
st.sidebar.markdown("---")

if radio_selection == 'Pipeline Explorer':
    pipeline_explorer.pipeline()
