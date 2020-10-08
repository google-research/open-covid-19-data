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

TODAYS_DATE=$(date "+%Y-%m-%d")
echo $TODAYS_DATE
BASE_FILE_PATH="./data/inputs/downloaded/search_trends_symptoms_dataset"
TODAY_FILE_PATH="$BASE_FILE_PATH/$TODAYS_DATE"
RAW_FILE_PATH="$BASE_FILE_PATH/raw_files"
echo $RAW_FILE_PATH
mkdir -p $RAW_FILE_PATH
mkdir -p $TODAY_FILE_PATH
gsutil cp -r gs://covid-st-prod-datasets-github/*/*/*/2020* $RAW_FILE_PATH
python ./src/scripts/fetch_search_trends.py --input_dir $RAW_FILE_PATH --output_dir $TODAY_FILE_PATH

shopt -s extglob
rm -r $BASE_FILE_PATH/!($TODAYS_DATE|LICENSE|README.md)/
