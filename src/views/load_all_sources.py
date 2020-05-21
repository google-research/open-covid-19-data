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
import yaml
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
PIPELINE_DIR = os.path.join(ROOT_DIR, 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import load_functions
import config


config = config.read_config()

st.title('Load all data sources:')

# Returns a dict where each key is a source and each value is a df
def load_all_data_sources():
    data = {}
    for k in config:
        params = config[k]
        load_func_name = params['load']['function']
        st.subheader(k)
        if load_func_name == 'None':
            st.write('No load function')
        else:
            load_func = getattr(load_functions, load_func_name)
            df = load_func(params)
            data[k] = df
            st.write(df)
    return data

load_all_data_sources()
