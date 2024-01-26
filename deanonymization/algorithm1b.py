# -*- coding: utf-8 -*-
"""
Created on Thu January 14 17:31:18 2023

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import pandas as pd
import numpy as np

def score_function(auxiliary_information, records):
    """
    This function calculates the score for a record r based on its similarity to the auxiliary information aux.

    Parameters:
    aux (dict): The auxiliary information.
    r (dict): The record.

    Returns:
    float: The score for the record.
    """

    score = 0
    # Specify the value you want to count
    value_to_count = '5167'

    # Count occurrences of the specified value in the dictionaries
    supp = sum(value_to_count in d.values() for d in my_list_of_dicts)
    for r in records:
        for aux in auxiliary_information:
            r+aux

    return score

def matching_criterion(scores, eccentricity):
    """
    This function determines whether there is a match based on the scores of the records.

    Parameters:
    scores (list): The scores of the records.

    Returns:
    bool: True if there is a match, False otherwise.
    """
    sorted_scores = sorted(scores)
    max_score = sorted_scores[0]
    max2_score = sorted_scores[1]
    sigma = np.std(scores)
    if (max_score - max2_score) / sigma < eccentricity:
        return False
    else:
        return True

def record_selection(scores, sigma):
    """
    This function selects the "best-guess" record or a probability distribution based on the scores.

    Parameters:
    scores (list): The scores of the records.

    Returns:
    dict or list: The "best-guess" record or a probability distribution.
    """
    if len(scores) == 1:
        return scores[0]
    else:
        probability_distribution = {}
        for i, score in enumerate(scores):
            probability_distribution[i] = np.exp(score / sigma)
        return probability_distribution

def algorithm_1b(aux, dataset):
    """
    This function de-anonymizes a target using auxiliary information.

    Parameters:
    aux (dict): The auxiliary information.
    dataset (DataFrame): The dataset.

    Returns:
    dict or list: The "best-guess" record or a probability distribution.
    """
    scores = []
    for record in dataset.to_dict('records'):
        score = score_function(aux, record)
        scores.append(score)

    record = record_selection(scores, 0.3)
    return record


# Load nf.csv and ml.csv datasets
nf_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA"
                        "\\BA-Implementierung\\datasets\\Netflix.csv",
                     header=None, encoding="UTF-8", sep = ";", nrows=10)

ml_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA"
                        "\\BA-Implementierung\\datasets\\MovieLens.csv",
                     header=None, encoding="UTF-8", sep = ";", nrows=10)

auxiliary_information = ml_df.to_dict("records")
auxiliary_information.pop(0)

records = nf_df.to_dict("records")
records.pop(0)

#{0: 'userId', 1: 'movieId', 2: 'rating', 3: 'timestamp'}
print(auxiliary_information)
#{0: 'userId', 1: 'rating', 2: 'timestamp', 3: 'movieId'}
print(records)

my_list_of_dicts = [
    {0: 'userId', 1: 'rating', 2: 'timestamp', 3: 'movieId'},
    {0: '1109700', 1: '4.0', 2: '1015.0', 3: '5167'},
    {0: '1056998', 1: '5.0', 2: '2283.0', 3: '5167'},
    {0: '903692', 1: '3.0', 2: '2295.0', 3: '5167'},
    # ... other dictionaries
]

# Specify the value you want to count
value_to_count = '5167'

# Count occurrences of the specified value in the dictionaries
count_occurrences = sum(value_to_count in d.values() for d in my_list_of_dicts)

print(f"The value '{value_to_count}' occurs {count_occurrences} times.")












