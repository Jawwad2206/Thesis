# -*- coding: utf-8 -*-
"""
Created on Thu Decemeber 14 17:31:18 2023

@author: Jawwad Khan, 7417247, Thesis Cybersecurity, Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import numpy as np
import pandas as pd
import datetime
import preprocessing.datasets as ld


def normalize_time():
    db = ld.load_DB_csv()
    db["rating"] = np.ceil(db["rating"])

    df = ld.load_DF_csv()

    # Create new reference time
    ref = datetime.datetime.strptime('19981001', '%Y%m%d')

    # Convert timestamp in DB
    temp_db = np.floor((pd.to_datetime(db["timestamp"], unit='s', origin='unix') - ref) / np.timedelta64(1, 'D'))
    db["timestamp"] = temp_db

    # Convert timestamp in DF
    temp_df = np.floor((pd.to_datetime(df["timestamp"], format='%Y-%m-%d') - ref) / np.timedelta64(1, 'D'))
    df["timestamp"] = temp_df

    db.to_csv("datasets\\MovieLens.csv", ";", index=False)
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

# Example usage
date_str1 = "1998-10-01"
date_str2 = "2001-12-31"

result = days_between_dates(date_str1, date_str2)
print(f"Days passed between {date_str1} and {date_str2}: {result} days")

