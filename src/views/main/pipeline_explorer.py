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

PIPELINE_DIR = os.path.join(os.path.dirname(__file__), '../../../', 'src/pipeline')

sys.path.append(PIPELINE_DIR)

import load_functions
import config
import plot_utils


def selected_data_types_to_cols(selected_data_types, data_params):
    if selected_data_types:
        filtered_data_params = {sdt: data_params[sdt] for sdt in selected_data_types}
    else:
        filtered_data_params = data_params
    filtered_data_cols = config.col_params_to_col_list(filtered_data_params)
    return filtered_data_cols

def get_filtered_df(df, data_params, filtered_data_types, filtered_region_level):
    identifier_list = ['date', 'region_code']
    region_list = ['parent_region_code', 'region_code_type', 'region_code_level',
                   'level_1_region_code', 'level_2_region_code', 'level_3_region_code']
    # identifiers = identifier_list + region_list
    if filtered_region_level != 'All':
        df = df[df['region_code_level'] == filtered_region_level]
    filtered_data_cols = selected_data_types_to_cols(filtered_data_types, data_params)
    filtered_columns = identifier_list + filtered_data_cols + region_list
    if 'test_units' in filtered_columns:
        filtered_columns.remove('test_units')
    filtered_df = df[filtered_columns]
    return filtered_df

def pipeline():
    config_dict = config.read_config(cc_by_sa=True)

    selected_sources = st.sidebar.multiselect('Data Source: ', list(config_dict.keys()))

    if not selected_sources:
        st.subheader('Click the arrow in top left to open the sidebar and select a data source!')

    selected_config = {selected_key: config_dict[selected_key] for selected_key in selected_sources}

    show_config = st.sidebar.checkbox('Show config', value=False, key='key1')
    show_load_function_output = st.sidebar.checkbox('Show load function output', value=True, key='key2')
    filtered_region_level = st.sidebar.radio('Filter by region levels', [1, 2, 3, 'All'])

    for k in selected_config:
        st.header('Data source: ' + k)
        params = config_dict[k]
        data_params = params['data']
        del data_params['testing']['units']  # hack: these are strings and mess up the plots, just remove them
        data_keys = list(data_params.keys())
        filtered_data_types = st.sidebar.multiselect('Filter ' + k + ' by data type:', data_keys)
        if show_config:
            st.subheader('Config: ')
            st.write(params)
        load_func_name = params['load']['function']
        if load_func_name == 'None':
            st.write('No load function')
        else:
            load_func = getattr(load_functions, load_func_name)
            df = load_func(params)
            if show_load_function_output:
                st.subheader('Load function output:')
                st.write(df)
            st.subheader('Filtered data:')
            #show_regions = st.checkbox('Filter by region level', value=False, key='key3')
            #filtered_region_level = st.checkbox('Filter by region level', value=False, key='key3')
            filtered_df = get_filtered_df(df, data_params, filtered_data_types, filtered_region_level)
            st.write(filtered_df)
        plot_data_types = st.sidebar.multiselect('Plot ' + k + ' by data type:', data_keys)
        plot_data_cols = selected_data_types_to_cols(plot_data_types, data_params)
        unique_regions = df.region_code.unique()
        # selected_regions = st.sidebar.multiselect('Select regions:', unique_regions)
        for region in unique_regions:
            st.write(region)
            region_df = df[df['region_code'] == region]
            source_df = plot_utils.melt_and_filter_data(plot_data_cols, region_df)
            st.altair_chart(plot_utils.ruled_altair_chart(source_df), use_container_width=True)
