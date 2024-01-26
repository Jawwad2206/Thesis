# -*- coding: utf-8 -*-
"""
Created on Thu December 14 17:31:18 2023

@author: Jawwad Khan,7417247,Thesis Cybersecurity,Title:The Role of the Adversary's Success Rate Metric in Cybersecurity

This module loads all the required datasets.
"""

import pandas as pd


def load_training_ml():
    """
    loads the original MovieLens dataset.
    The dataset can be downloaded from https://grouplens.org/datasets/movielens/20m/

    The dataset should be downloaded into the dataset directory for smoother operations.

    :return: df -> dataframe object of MovieLens
    """
    # Load the MovieLens dataset as panda DataFrame

    df = pd.read_csv("datasets\\ml-20m\\ratings.csv",
                     header=0, encoding="UTF-8", dtype={0: int, 1: int, 2: float, 3: float},
                     names=["userId", "movieId", "rating", "timestamp"])
    return df

def load_ml_csv():
    """
    load the pre-processed (adjusted to be in the same shape as the Netflix dataset) MovieLens dataset.

    :return: dataframe object of the pre-processed MovieLens dataset
    """
    # Load the pre-processed MovieLens
    db = pd.read_csv("datasets\\ml.csv", encoding="UTF-8", sep=";")

    return db

def load_nf_csv():
    """
    load the pre-processed Netflix dataset.

    :return: dataframe object of the pre-processed Netflix dataset
    """
    # Load the pre-processed Netflix dataset as panda DataFrame
    db = pd.read_csv("datasets\\nf.csv", encoding="UTF-8", sep=";")
    # drops all entries that include a NaN Column
    db = db.dropna()

    return db


