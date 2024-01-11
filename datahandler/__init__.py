# -*- coding: utf-8 -*-
"""
Created on Thu Januar 11 16:51:18 2024

@author: Jawwad Khan, 7417247, Thesis Cybersecurity, Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import pandas as pd
import numpy as np
from datetime import datetime
import time

def load_training():
    # Load the original dataset
    df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA\\ml-20m\\ml-20m\\ratings.csv")
    return df
