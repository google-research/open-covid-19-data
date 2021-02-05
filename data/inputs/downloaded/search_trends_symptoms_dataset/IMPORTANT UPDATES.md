## Dataset updates
On Dec 15, 2020 we made several changes to the dataset:
1. To make it easier to compare a wider range of symptoms within the same region, whenever daily data is available we now also produce an aggregate weekly value computed from the individual daily (Monday to Sunday) values. The method is described in the [updated documentation](https://storage.googleapis.com/gcp-public-data-symptom-search/COVID-19%20Search%20Trends%20symptoms%20dataset%20documentation%20.pdf).
2. To account for the newly available weekly-from-daily data, we adopted a new scaling factor for all US symptoms reported in the weekly time series. While the numbers for normalized search volume changed, the normalized search volumes retain their interpretation relative to each other. Please delete any previously downloaded weekly files and download the fresh files to maintain consistency in the data.
3. We are making the CSVs available to download as part of our [interactive charts page](https://pair-code.github.io/covid19_symptom_dataset). We will not be directly hosting the CSV files in this repository going forward.
4. We have expanded the dataset to include the following regions: Australia, Ireland, New Zealand, Singapore, and the United Kingdom.

## Feedback
If you have any questions on these updates please email us at covid-19-search-trends-feedback@google.com.
