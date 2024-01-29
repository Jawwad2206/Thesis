# -*- coding: utf-8 -*-
"""
Created on Thu January 14 17:31:18 2023

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""
import pandas
import pandas as pd
import numpy as np
from collections import Counter as ct
def score_function(aux, record, counts):
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
    rating = float(record.get(1))
    timestamp = float(record.get(2))
    aux_rating = float(aux.get(2))
    aux_timestamp = float(aux.get(3))

    if aux_timestamp < 0:
        score = 0
    else:
        wt = (1/(np.log10(counts)))
        score = wt * (np.exp(-((abs(aux_rating - rating)) / rho0)) + np.exp(-((abs(aux_timestamp - timestamp)) / d0)))

    return score

def matching_criterion(scores, eccentricity):
    """
    This function determines whether there is a match based on the scores of the records.

    Parameters:
    scores (list): The scores of the records.

    Returns:
    bool: True if there is a match, False otherwise.
    """
    if (sum(scores) == 0):
        return False, 0, 0
    else:
        sorted_scores = sorted(scores, reverse=True)
        #print(sorted_scores, "sorted scores")
        unique_list = list(sorted(set(sorted_scores), reverse=True))
        #print(unique_list, "unique List")
        max_score = unique_list[0]
        #print(max_score, "S1")
        max2_score = unique_list[1]
        #print(max2_score, "S2")
        sigma = np.std(scores)
        #print(sigma, "sigma")
        #print((max_score - max2_score) / sigma, "eccentricity")
        if (max_score - max2_score) / sigma < eccentricity:
            return False, max_score, ((max_score - max2_score) / sigma)
        else:
            return True, max_score, ((max_score - max2_score) / sigma)

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

def algorithm_1b(com_movie, counts_movie,ml_df, nf_df):
    """
    This function de-anonymizes a target using auxiliary information.

    Parameters:
    aux (dict): The auxiliary information.
    dataset (DataFrame): The dataset.

    Returns:
    dict or list: The "best-guess" record or a probability distribution.
    """

    eccentricity = 0.5
    for id in com_movie:
        auxalso = []
        records_i = nf_df.loc[id,:]
        auxiliary_information_i = ml_df.loc[id,:]
        records = records_i.to_dict("records")
        if isinstance(auxiliary_information_i, pandas.Series):
            auxiliary_information = auxiliary_information_i.to_dict()
            auxalso.append(auxiliary_information)
            auxiliary_information = auxalso
        else:
            auxiliary_information = auxiliary_information_i.to_dict("records")
        for aux in auxiliary_information:
            scores = []
            #print(aux, "aux")
            print("Auxiliary Information ->", aux)
            for record in records:
                #print(record, "record")
                #print(counts_movie.get(id), "counts_movie.get(id)")
                score = score_function(aux, record, counts_movie.get(id))
                scores.append(score)
            match, max_score, ecc = matching_criterion(scores, eccentricity)
            print("------------------------------------------")
            if match == True:
                pd = record_selection(scores)
                for i in range(len(scores)):
                    if scores[i] == max_score:
                        print("->Record:", i, "Score:", round(scores[i], 2), "Max Score:", round(max_score, 2),
                              "Set Eccentricity:", eccentricity, "Calculated Eccentricity", round(ecc,2),
                              "Probability:", round(pd.get(i), 2), "Candidate Record-->:", records[i])
                    else:
                        print("->Record:", i, "Score:", round(scores[i], 2), "Max Score:", round(max_score, 2),
                              "Set Eccentricity:", eccentricity,"Calculated Eccentricity", round(ecc,2), "Probability:",
                              round(pd.get(i), 2))
                print("\n")
            elif max_score == 0 and ecc == 0:
                print("no match error in row!")
                print("\n")
            else:
                print("no match Eccentricity:", round(ecc, 2), "<", eccentricity)
                print("\n")






# Load nf.csv and ml.csv datasets

nf_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA"
                    "\\BA-Implementierung\\datasets\\Netflix.csv",
                     header=None, encoding="UTF-8", sep = ";", skiprows=1, nrows=3600)

nf_df_dict = nf_df.to_dict("records")


ml_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\"
                    "7.Semester\\BA\\BA-Implementierung\\datasets\\MovieLens.csv",
                     header=None, encoding="UTF-8", sep = ";", skiprows=1, nrows=3000)




#{0: 'userId', 1: 'movieId', 2: 'rating', 3: 'timestamp'},
auxi_test  = [
    {0: '1', 1: '50', 2: '4.0', 3: '2375.0'},
    {0: '1', 1: '151', 2: '4.0', 3: '2171.0'},
    {0: '1', 1: '5167', 2: '5.0', 3: '2171.0'},
    {0: '1', 1: '5167', 2: '3.0', 3: '2312.0'},
    {0: '1', 1: '5168', 2: '4.0', 3: '2575.0'}
]
#{0: '1', 1: '5168', 2: '1.0', 3: '1175.0'},

#{0: 'userId', 1: 'rating', 2: 'timestamp', 3: 'movieId'},
records_test = [
    {0: '1109700', 1: '4.0', 2: '1015.0', 3: '5167'},
    {0: '1056998', 1: '5.0', 2: '2283.0', 3: '5167'},
    {0: '903692', 1: '3.0', 2: '2295.0', 3: '5167'},
    {0: '2380973', 1: '4.0', 2: '2603.0', 3: '5167'},
    {0: '497196', 1: '3.0', 2: '1975.0', 3: '5167'},
    {0: '74144', 1: '3.0', 2: '2312.0', 3: '5167'},
    {0: '2075969', 1: '5.0', 2: '2443.0', 3: '5167'},
    {0: '2535052', 1: '4.0', 2: '2575.0', 3: '5168'},
    {0: '76196', 1: '1.0', 2: '1175.0', 3: '5168'}
]

#count_movie = ct(entry[3] for entry in records_test)
count_movie = ct(entry[3] for entry in nf_df_dict)
#deafen = pd.DataFrame(records_test)
#dafen = pd.DataFrame(auxi_test)
deafen = nf_df
dafen = ml_df
deafen.set_index([3],inplace=True) # setze movieID als index also haupterkennung
dafen.set_index([1],inplace=True) # setze movieID als index also haupterkennung
com_movies = deafen.index.unique().intersection(dafen.index.unique()) # gib nur die MovieIDs die beide haben



algorithm_1b(com_movies, count_movie, dafen, deafen)










