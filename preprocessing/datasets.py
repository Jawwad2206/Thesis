# -*- coding: utf-8 -*-
"""
Created on Thu Decemeber 14 17:31:18 2023

@author: Jawwad Khan, 7417247, Thesis Cybersecurity, Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import pandas as pd


def load_training_ml():
    # Load the original dataset
    df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA\\ml-20m\\ml-20m\\ratings.csv", header=None, encoding="UTF-8", names=["userId","movieId","rating","timestamp"])
    return df