# Covid Cab

> This project aims to solve the final challenge in days 4-6 of TalkPython's [100DaysOfCode in Python](https://training.talkpython.fm/courses/details/100-days-of-code-in-python) course.
> The challenge was to use a public dataset to practice using the [Collections](https://docs.python.org/3/library/collections.html) module.

The script utilises the [New York City TLC Trip Record Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) datasets, specifically the Yellow Taxi Trip Records for April 2020.

The dataset used in this repo has been cut down to the first week in April 2020, and parses data to generate information about Yellow Taxi journeys taken in New York during this time period.

The significant thing about this time period is that is was in the middle of a COVID-19 state-wide lockdown for New York. The information returned covers the following areas:

* Total distance, fares and passengers for every taxi vendor.
* Average distance, fare and passenger count per taxi vendor.
* A list of the top 50 journeys sorted in descending order by distance for each taxi vendor.
