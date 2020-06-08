# How to Contribute

This project wouldn't exist without the contributions from many volunteers around the world, who find data sources, contact data owners, translate languages, scrape data, build visualizations, and more.

We'd love for you to join this project and we're excited to accept your patches and contributions! Here are a few guidelines that we ask you to follow.

## Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License
Agreement. You (or your employer) retain the copyright to your contribution;
this simply gives us permission to use and redistribute your contributions as
part of the project. Head over to <https://cla.developers.google.com/> to see
your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one
(even if it was for a different project), you probably don't need to do it
again.

## Submitting bug fixes
If you notice a bug, please feel free to submit an issue, or even better, a pull request to fix it! You can find more information on using pull requests on [GitHub Help](https://help.github.com/articles/about-pull-requests/).

## Adding New Data Sources
We are interested in including any public data sources that are useful for COVID-19 modeling. We are only able to include data sources where there is licensing information available on the data, or we are able to contact the data owners to obtain their consent.

##### Step 1:
If you find a data source that you'd like to see included, please send an email to open-covid-19-data@google.com including the following information:
- **Source URL:** URL of the page containing data
- **License URL or contact email:** If you are able to find a page containing any license info, please include the url here. If not, you can also include a contact email address or a link to a page containing contact info. If neither of these are available, you can leave this blank and we will do our best to locate the information we need.
- **Data format:** whether this data can be downloaded as a csv/xslx, or needs to be read by a human
- **English translations, if possible:** If the descriptions about the data are in a language other than English and you're able to provide an English translation of the relevant descriptions or column names, please include that here.
- **Whether you'd like to write the pull request to ingest the data:** If you'd like to write the code to ingest the data, let us know and we will notify you when the data is approved for ingestion, so that you can submit a PR that ingests the data into the pipeline. We are also happy to do this step if you just want the data included for your use.

##### Step 2:
Once we confirm that the licensing on the data is okay to include in this project, we will open an issue to ingest the data, along with what information to include in the attribution and licensing section.

##### Step 3:
From there, you can follow the instructions in the README that describes the technical steps to add new data sources - this generally requires writing a yaml config file for the data source and sometimes additional python functions if the data formatting contains edge cases. Please feel free to respond in the issue if you have questions during this step.


## Adding New Features
If you'd like to add a new feature to this repository, please first create a github issue with a short description of what you'd like to add and how you might implement it, and we will respond in the issue with any feedback and let you know when you should move ahead! We'd love to encourage your contributions but don't want you to be disappointed if you work hard on a pull request that isn't quite right for us to merge and we have to ask you to alter a significant piece of your work.

## Community Guidelines

This project follows
[Google's Open Source Community Guidelines](https://opensource.google/conduct/).
