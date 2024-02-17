# -*- coding: utf-8 -*-
"""
Created on Thu December 14 17:31:18 2023

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity

This module contains all the function related to the time manipulation of csvs.

This code is based on the code of BigBrother

Source :https://github.com/mpetitjean/BigBrother/blob/master/src/Timestamp%20normalization.ipynb
(Accessed: Thu December 14 17:31:18 2023)

The code had to be adjusted because of old dependencies and use case.
"""

import numpy as np
import pandas as pd
import datetime
import preprocessing.datasets as ld



def normalize_time():
    """
    This module normalizes the timestamps for Netflix and MovieLens datasets.

    This function loads the dataframes of Netflix and MovieLens, normalizes the timestamp column to represent days since
    a reference time, and rounds up the ratings to the nearest integer. The modified dataframes are
    then saved to separate CSV files.

    This code is based on the code of BigBrother

    Source :https://github.com/mpetitjean/BigBrother/blob/master/src/Timestamp%20normalization.ipynb
    (Accessed: Thu December 14 17:31:18 2023)

    The code had to be adjusted because of old dependencies and use case.
    """
    # Load another dataframe containing the pre-processed MovieLens dataset
    db = ld.load_ml_csv()

    # Round up the ratings to the nearest integer
    db["rating"] = np.ceil(db["rating"])

    # Load another dataframe containing the pre-processed Netflix dataset
    df = ld.load_nf_csv()

    # Create a reference time object based on the date '19981001'
    ref = datetime.datetime.strptime('19981001', '%Y%m%d')

    # Convert timestamp in the database dataframe to days since the reference time
    temp_db = np.floor((pd.to_datetime(db["timestamp"], unit='s', origin='unix') - ref) / np.timedelta64(1, 'D'))
    db["timestamp"] = temp_db

    # Convert timestamp in the dataframe to days since the reference time
    temp_df = np.floor((pd.to_datetime(df["timestamp"], format='%Y-%m-%d') - ref) / np.timedelta64(1, 'D'))
    df["timestamp"] = temp_df

    # Save the modified movie ratings database to a new CSV file with a specified delimiter
    db.to_csv("datasets\\MovieLens.csv", ";", index=False)

    # Save the modified dataframe to a new CSV file with a specified delimiter
    df.to_csv("datasets\\Netflix.csv", ";", index=False)

def days_between_dates(date_str1, date_str2):
    date_format = "%Y-%m-%d"

    # Convert date strings to datetime objects
    date1 = datetime.datetime.strptime(date_str1, date_format)
    date2 = datetime.datetime.strptime(date_str2, date_format)

    # Calculate the difference between the two dates
    delta = date2 - date1

    # Extract the number of days from the timedelta object
    days_passed = delta.days

    return days_passed



