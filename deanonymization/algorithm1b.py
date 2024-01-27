# -*- coding: utf-8 -*-
"""
Created on Thu January 14 17:31:18 2023

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import pandas as pd
import numpy as np

def score_function(aux, record, supp):
    """
    This function calculates the score for a record r based on its similarity to the auxiliary information aux.

    Parameters:
    aux (dict): The auxiliary information.
    r (dict): The record.

    Returns:
    float: The score for the record.
    """
    score = 0
    rho0 = 1.5
    d0 = 30
    #user_id = record.get(0)
    rating = float(record.get(1))
    timestamp = float(record.get(2))
    #aux_user_id = aux.get(0)
    #aux_movie_id = aux.get(1)
    aux_rating = float(aux.get(2))
    aux_timestamp = float(aux.get(3))


    if supp == 0 or supp == 1:
        print("schade")
    else:
        wt = (1/(np.log(supp)))
        e1 = -((abs(aux_rating - rating)) / rho0)
        e2 = -((abs(aux_timestamp - timestamp)) / d0)
        score = wt * (np.exp(e1) + np.exp(e2))

    return score

def matching_criterion(scores, eccentricity):
    """
    This function determines whether there is a match based on the scores of the records.

    Parameters:
    scores (list): The scores of the records.

    Returns:
    bool: True if there is a match, False otherwise.
    """
    sorted_scores = sorted(scores, reverse=True)
    #print(sorted_scores, "sorted scores")
    unique_list = list(set(sorted_scores))
    max_score = unique_list[0]
    #print(max_score, "S1")
    max2_score = unique_list[1]
    #print(max2_score, "S2")
    sigma = np.std(scores)
    #print(sigma, "sigma")
    #print((max_score - max2_score) / sigma)
    if (max_score - max2_score) / sigma < eccentricity:
        return False
    else:
        return True, max_score

def record_selection(scores):
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
        std_dev = np.std(scores)
        c = 1 / np.sum(np.exp(scores / std_dev))
        for i, score in enumerate(scores):
            probability_distribution[i] = c * (np.exp(score / std_dev))
        return probability_distribution

def algorithm_1b(auxiliary_information, records):
    """
    This function de-anonymizes a target using auxiliary information.

    Parameters:
    aux (dict): The auxiliary information.
    dataset (DataFrame): The dataset.

    Returns:
    dict or list: The "best-guess" record or a probability distribution.
    """
    count = 0
    eccentricity = 0.7
    for record in records:
        count += 1
        scores = []
        movie_id = record.get(3)
        print("Record",count, record)
        print("|-----------------------------|")
        for aux in auxiliary_information:
            supp = sum(d.get(1) == movie_id for d in auxiliary_information)
            score = score_function(aux, record, supp)
            scores.append(score)
        match, max_score = matching_criterion(scores, eccentricity)
        if match == True:
            pd = record_selection(scores)
            for i in range(len(scores)):
                print("->Aux:", i, "Score:", round(scores[i],2),"Max Score:", round(max_score, 2), "Eccentricity:", eccentricity, "Probability:", round(pd.get(i), 2))
        else:
            print("no match found!")




# Load nf.csv and ml.csv datasets

nf_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA"
                    "\\BA-Implementierung\\datasets\\Netflix.csv",
                     header=None, encoding="UTF-8", sep = ";", nrows=10)


ml_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\"
                    "7.Semester\\BA\\BA-Implementierung\\datasets\\MovieLens.csv",
                     header=None, encoding="UTF-8", sep = ";", nrows=10)

auxiliary_information = ml_df.to_dict("records")
auxiliary_information.pop(0)


records = nf_df.to_dict("records")
records.pop(0)



#{0: 'userId', 1: 'movieId', 2: 'rating', 3: 'timestamp'},
auxi_test  = [
 {0: '1', 1: '5167', 2: '2.0', 3: '2305.0'},
 {0: '1', 1: '5167', 2: '4.0', 3: '2395.0'},
 {0: '1', 1: '5167', 2: '4.0', 3: '2171.0'},
 {0: '1', 1: '5167', 2: '1.0', 3: '2560.0'},
 {0: '1', 1: '5167', 2: '4.0', 3: '2375.0'},
 {0: '1', 1: '5167', 2: '4.0', 3: '2171.0'},
 {0: '1', 1: '5167', 2: '5.0', 3: '2443.0'},
 {0: '1', 1: '5167', 2: '2.0', 3: '2843.0'},
 {0: '1', 1: '5167', 2: '3.0', 3: '2171.0'}
         ]

#{0: 'userId', 1: 'rating', 2: 'timestamp', 3: 'movieId'},
records_test = [
        {0: '1109700', 1: '4.0', 2: '2375.0', 3: '5167'}
            ]




algorithm_1b(auxiliary_information, records)












