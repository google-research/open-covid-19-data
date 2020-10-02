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

import altair as alt

def ruled_altair_chart(source):
    line = alt.Chart(source).encode(
        x=alt.X('yearmonthdate(date):T', axis=alt.Axis(tickSize=0, labelAngle=-90, tickCount=5, title='Date')),
        y=alt.Y('value', title='Count'),
        color='variable'
    )
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['date'], empty='none')
    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(source).mark_point().encode(x='date', opacity=alt.value(0)).add_selection(nearest)
    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))
    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(text=alt.condition(nearest, 'value:Q', alt.value(' ')))
    # Draw a rule at the location of the selection
    rules = alt.Chart(source).mark_rule(color='gray').encode(x='date',).transform_filter(nearest)
    # Put the five layers into a chart and bind the data
    layers = alt.layer(line.mark_line(), selectors, points, text, rules)

    return layers

def melt_and_filter_data(columns, df):
    plot_df = df[columns + ['date']]
    source_df = plot_df.reset_index().melt('date')
    source_df = source_df[source_df['variable'] != 'index']
    return source_df
