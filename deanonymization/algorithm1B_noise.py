# -*- coding: utf-8 -*-
"""
Created on Thu January 14 17:31:18 2023

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import pandas as pd
import numpy as np
from collections import Counter as ct
import matplotlib.pyplot as plt


def sim(rating, timestamp, aux_rating, aux_timestamp):
    sim_score = 0

    if abs(aux_timestamp - timestamp) <= 14:
        if abs(aux_timestamp - timestamp) <= 3:
            sim_score += 1
        else:
            sim_score += 0
    else:
        sim_score += 0

    if abs(rating - aux_rating) == 0:
        sim_score += 1
    else:
        sim_score += 0

    return sim_score

def score_function(aux, record, counts):
    """
    This function calculates the score for a record r based on its similarity to the auxiliary information aux.

    Parameters:
    aux (dict): The auxiliary information.
    r (dict): The record.

    Returns:
    float: The score for the record.
    """
    sim_score = 0
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
        sim_score = sim(rating, timestamp, aux_rating, aux_timestamp)
        wt = (1/(np.log10(counts)))
        score = wt * (np.exp(-((rating - rating)) / rho0) + np.exp((-aux_timestamp - timestamp) / d0))

    return score + sim_score

def matching_criterion(scores, eccentricity):
    """
    This function determines whether there is a match based on the scores of the records.

    Parameters:
    scores (list): The scores of the records.

    Returns:
    bool: True if there is a match, False otherwise.
    """
    if (sum(scores) == 0):
        #print("case 1")
        return False, 0, 0
    elif len(scores) == 1:
        #print("case 2")
        max_score = scores[0]
        if max_score < 2:
            return False, max_score, max_score
        else:
            return False, max_score, max_score
    else:
        #print("case 3")
        sorted_scores = sorted(scores, reverse=True)
        #print(sorted_scores)
        #print(sorted_scores, "sorted scores")
        unique_list = list(sorted(set(sorted_scores), reverse=True))
        #print(unique_list, "unique List")
        max_score = unique_list[0]
        #print(max_score, "S1")
        max2_score = unique_list[1]
        #print(max2_score, "S2")
        sigma = np.std(scores)
        #print(sigma, "sigma")
        #print(((max_score - max2_score) / sigma), "eccentricity")
        ecc_calc = ((max_score - max2_score) / sigma)
        if ecc_calc < eccentricity:
            return False, max_score, ecc_calc
        else:
            return True, max_score, ecc_calc

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

    eccentricity = 2
    list_ecc = []
    match_true = 0
    match_false = 0
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
        for record in records:
            scores = []
            print("MovieID:", id, "Record ->", record)
            for aux in auxiliary_information:
                #print(record, "record")
                #print(counts_movie.get(id), "counts_movie.get(id)")
                score = score_function(aux, record, counts_movie.get(id))
                scores.append(score)
            match, max_score, ecc = matching_criterion(scores, eccentricity)
            print("------------------------------------------")
            if match == True:
                match_true +=1
                if max_score == ecc:
                    continue
                else:
                    list_ecc.append(ecc)
                pd = record_selection(scores)
                for i in range(len(scores)):
                    if scores[i] == max_score:
                        print("->Record:", i, "Score:", round(scores[i], 2), "Max Score:", round(max_score, 2),
                              "Set Eccentricity:", eccentricity, "Calculated Eccentricity", round(ecc,2),
                              "Probability:", pd.get(i), "Candidate Record-->:", auxiliary_information[i])
                    else:
                        print("->Record:", i, "Score:", round(scores[i], 2), "Max Score:", round(max_score, 2),
                              "Set Eccentricity:", eccentricity,"Calculated Eccentricity", round(ecc,2), "Probability:",
                              pd.get(i), "Candidate Record-->:", auxiliary_information[i])
                print("\n")
            elif max_score == 0 and ecc == 0 or max_score == ecc:
                match_false += 1
                print("no match")
                print("\n")
            else:
                match_false += 1
                print("no match Eccentricity:", round(ecc, 2), "<", eccentricity)
                print("\n")



    return list_ecc, match_true, match_false



# Load nf.csv and ml.csv datasets

nf_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA"
                    "\\BA-Implementierung\\datasets\\Netflix.csv",
                     header=None, encoding="UTF-8", sep = ";", skiprows=1, nrows=100000)

nf_df_dict = nf_df.to_dict("records")


ml_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\"
                    "7.Semester\\BA\\BA-Implementierung\\datasets\\MovieLens.csv",
                     header=None, encoding="UTF-8", sep = ";", skiprows=1, nrows=100000)

ml_df_dict = ml_df.to_dict("records")


#{0: 'userId', 1: 'movieId', 2: 'rating', 3: 'timestamp'},
auxi_test  = [
    {0: '1', 1: '50', 2: '4.0', 3: '2375.0'},
    {0: '1', 1: '151', 2: '4.0', 3: '2171.0'},
    {0: '1', 1: '5167', 2: '5.0', 3: '2283.0'},
    {0: '1', 1: '5167', 2: '3.0', 3: '2812.0'},
    {0: '1', 1: '5168', 2: '5.0', 3: '2575.0'}
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


list_ecc, match_true, match_false = algorithm_1b(com_movies, count_movie, dafen, deafen)
count_ecc = ct(list_ecc)
print(count_ecc)
def create_histogram(list_ecc):
    # Generate some random data
    data = list_ecc  # You can replace this with your own dataset
    # Create a histogram
    plt.hist(data, bins=30, edgecolor='black')

    # Adding labels and title
    plt.xlabel('Eccentricity Φ')
    plt.ylabel('# Matches')
    plt.title("Distribution of Eccentricity Φ")

    # Display the histogram
    plt.show()

def create_barchart(match_true, match_false):
    # Sample data
    categories = ['Category A', 'Category B', 'Category C', 'Category D']
    values = [20, 35, 40, 25]

    # Creating a bar chart
    plt.bar(categories, values)

    # Adding labels and title
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Chart Example')

    # Display the chart
    plt.show()


create_histogram(list_ecc)