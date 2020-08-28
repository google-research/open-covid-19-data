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

PIPELINE_DIR = os.path.join(os.path.dirname(__file__), '../../../', 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import args_utils
import load_data
import config


args = args_utils.get_parser().parse_args()

config_dict = config.read_config(cc_by=True, cc_by_sa=True, google_tos=True, cc_by_nc=True,
                                 filter_by_fetch_method=None,
                                 filter_no_load_func=False,
                                 filter_no_data=False,
                                 filter_not_approved=args.allowlist)

if args.source:
    filtered_config_dict = {}
    for source in args.source:
        filtered_config_dict[source] = config_dict[source]
    config_dict = filtered_config_dict

st.title('Load all data sources:')

# Returns a dict where each key is a source and each value is a df
def load_all_data_sources():
    data = {}
    for k in config_dict:
        params = config_dict[k]
        load_func_name = params['load']['function']
        st.subheader(k)
        if load_func_name == 'None':
            st.write('No load function')
        else:
            df = load_data.load_most_recent_loadable_data(params)
            data[k] = df
            # Mobility reports are too large for streamlit to handle
            if k != 'google_mobility_reports':
                st.write(df)
    return data

load_all_data_sources()
