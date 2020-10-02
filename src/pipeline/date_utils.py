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

# pylint: disable=unused-argument

import pandas as pd
import datetime


def parse_date(data_df, params):
    date_parse_func = params['load']['dates']['parse_function']
    data_df = globals()[date_parse_func](data_df, params)
    return data_df

def default(data_df, params):
    date_params = params['load']['dates']
    date_columns = date_params['columns']
    date_column = date_columns[0]
    data_df = data_df.rename(columns={
        date_column: 'original_date'
    })
    if 'date_format' in date_params:
        date_format = date_params['date_format']
        data_df['date'] = pd.to_datetime(data_df['original_date'], format=date_format).dt.strftime('%Y-%m-%d')
    else:
        data_df['date'] = pd.to_datetime(data_df['original_date']).dt.strftime('%Y-%m-%d')
    return data_df

def luxembourg_hospitalization_dates(data_df, params):
    format1 = '%Y-%m-%d %h:%m:%s'
    format2 = '%d/%m/%Y'
    def fix_date(original):
        try:
            fixed = pd.to_datetime(original, format=format1).date().strftime('%Y-%m-%d')
        except ValueError:
            fixed = pd.to_datetime(original, format=format2).date().strftime('%Y-%m-%d')
        return fixed
    data_df['date'] = data_df['Date'].apply(fix_date)
    return data_df

def japan_hospitalization_dates(data_df, params):
    data_df = data_df.rename(columns={
        'date': 'day'
    })
    data_df['date'] = pd.to_datetime({
        'year': data_df['year'],
        'month': data_df['month'],
        'day': data_df['day']}).dt.strftime('%Y-%m-%d')
    return data_df

def netherlands_hospitalization_dates(data_df, params):
    def fix_date(original):
        day_str, month_str = original.split(' ')
        month_dict = {'feb': 2, 'mrt': 3, 'apr': 4, 'mei': 5, 'jun': 6}
        month = month_dict[month_str]
        year = 2020
        return datetime.date(year, month, int(day_str)).strftime('%Y-%m-%d')
    data_df['date'] = data_df['Datum ziekenhuisopname'].apply(fix_date)
    return data_df

def iceland_dates(data_df, params):
    data_df = data_df.rename(columns={
        data_df.columns[0]: 'original_date',
    })
    def fix_date(original):
        day_str, month_str = str(original).split('.')
        year = 2020
        return datetime.date(year, int(month_str), int(day_str)).strftime('%Y-%m-%d')
    data_df['date'] = data_df['original_date'].apply(fix_date)
    return data_df

def scotland_hospitalizations_dates(data_df, params):
    data_df = data_df.rename(columns={
        data_df.columns[0]: 'original_date',
    })
    data_df['date'] = pd.to_datetime(data_df['original_date']).dt.strftime('%Y-%m-%d')
    return data_df
