# -*- coding: utf-8 -*-
"""
Created on Thu Decemeber 14 17:31:18 2023

@author: Jawwad Khan, 7417247, Thesis Cybersecurity, Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import pandas as pd


def load_training_ml():
    # Load the MovieLens dataset
    df = pd.read_csv(
        "datasets\\ml-20m\\ratings.csv",
        header=0, encoding="UTF-8", dtype={0: int, 1: int, 2: float, 3: float},
        names=["userId", "movieId", "rating", "timestamp"])
    return df

def load_DB_csv():
    db = pd.read_csv("datasets\\ml.csv", encoding="UTF-8", sep=";")
    return db

def load_DF_csv():
    db = pd.read_csv("datasets\\nf.csv", encoding="UTF-8", sep=";")
    db = db.dropna()
    return db


