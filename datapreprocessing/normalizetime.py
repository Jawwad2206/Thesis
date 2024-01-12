# -*- coding: utf-8 -*-
"""
Created on Thu Decemeber 14 17:31:18 2023

@author: Jawwad Khan, 7417247, Thesis Cybersecurity, Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""
import pandas as pd
import numpy as np
import datetime

def normalize_time():
    db = pd.read_csv("DB.csv", encoding="UTF-8", sep=";")
    db["rating"] = np.ceil(db["rating"])
    db.head()
    df = pd.read_csv("DF.csv", encoding="UTF-8", sep=";")
    df.head()
    # Create new reference time
    ref = datetime.datetime.strptime('19981001', '%Y%m%d')

    temp_db = np.where(db["timestamp"].notna(), np.floor((db["timestamp"].apply(datetime.datetime.fromtimestamp) - ref) / datetime.timedelta(days=1)), np.nan)
    # db.head()
    # df.head()

    temp_df = np.where(df["timestamp"].notna(), np.floor((df["timestamp"].astype(str).apply(datetime.datetime.strptime, args=('%Y%m%d',)) - ref) / datetime.timedelta(days=1)), np.nan)

    db["timestamp"] = temp_db
    df["timestamp"] = temp_df
    db.to_csv("time_fixed_DB.csv", ";", index=False)
    df.to_csv("time_fixed_DF.csv", ";", index=False)