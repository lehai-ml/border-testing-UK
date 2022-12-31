# Findings of comparison of border testing results between the UK and other countries
Note: raw data not uploaded

Objectives:

Examining and visualising the differences in border testing results between the UK and other countries.

Methods:

Countries were selected for comparison if there exist information regarding COVID-19 border testing. Here, in addition to the UK, the following countries were examined: Korean, Thailand, Iceland, Israel and Canada. The data was pulled from multiple government sources and using the WayBack machine. Not all countries contained similar information, but exhaustive comparison with the UK data was done where possible. 

Files description:
* 1_File_preprocess.ipynb: Preprocess the downloaded data into a format for visualisation
* 2_UK_comparison.ipynb: Compare the border testing data between the UK and other countries
* analyses_code/preprocessing.py : all the preprocessing and visualising functions
* analyses_code/wayback_webscrapping.py: Function to scrape Korean daily positive cases data.
* dataset/preprocessed_data/* : Folders containing preprocessed data for each country. Used in the 2_UK_comparison.ipynb

Results:
![Border testing result](./output_plot/CanadavsUK.png "Figure 1. Border testing result between multiple countries")
Figure 1. Border testing result between multiple countries.
![Border moving test](./output_plot/border_moving_testing_ppt.png "Figure 2. Moving average")
Figure 2. Border testing moving average 70day incidence per 100 000 inhabitants
![Border test variants](./output_plot/border_test.png "Figure 3. Variants")
Figure 3. Variants comparison between UK and Canada
![Countries of arrivals](./output_plot/countries_of_interest.png "Figure 4. Countries of arrivals")
Figure 4. Countries of arrivals to Israel vs. the UK
