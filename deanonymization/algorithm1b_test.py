# -*- coding: utf-8 -*-
"""
Created on Thu January 14 17:31:18 2023

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import pandas
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

    if (aux_timestamp - timestamp) == 0 and (aux_rating - rating) == 0:
        sim_score += 10

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
        score = wt * (np.exp(-((aux_rating - rating)) / rho0) + np.exp((-aux_timestamp - timestamp) / d0))

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
        print("case 1")
        return False, 0, 0
    elif len(scores) == 1:
        print("case 2")
        max_score = scores[0]
        if max_score < 2:
            return False, max_score, max_score
        else:
            return False, max_score, max_score
    else:
        print("case 3")
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

def algorithm_1b(com_movie, counts_movie,ml_df, nf_df, dummy_records):
    """
    This function de-anonymizes a target using auxiliary information.

    Parameters:
    aux (dict): The auxiliary information.
    dataset (DataFrame): The dataset.

    Returns:
    dict or list: The "best-guess" record or a probability distribution.
    """

    eccentricity = 1.5
    list_ecc = []
    match_true = 0
    match_false = 0
    for id in com_movie:
        aux_list_one = []
        records_i = nf_df.loc[id,:]
        auxiliary_information_i = ml_df.loc[id,:]
        records = records_i.to_dict("records")
        if isinstance(auxiliary_information_i, pandas.Series):
            auxiliary_information = auxiliary_information_i.to_dict()
            aux_list_one.append(auxiliary_information)
            auxiliary_information = aux_list_one
        else:
            if id == 7149:
                auxiliary_information = (auxiliary_information_i.to_dict("records") + dummy_entries)
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
                        continue
                        #print("->Record:", i, "Score:", round(scores[i], 2), "Max Score:", round(max_score, 2),
                              #"Set Eccentricity:", eccentricity,"Calculated Eccentricity", round(ecc,2), "Probability:",
                              #pd.get(i), "Candidate Record-->:", auxiliary_information[i])
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


dummy_entries = [
{0: "1118663", 2: 4.0, 3: 2335.0},
{0: "686179", 2: 4.0, 3: 2336.0},
{0: "217912", 2: 4.0, 3: 2339.0},
{0: "989270", 2: 3.0, 3: 2340.0},
{0: "1113868", 2: 3.0, 3: 2341.0},
{0: "1227649", 2: 3.0, 3: 2341.0},
{0: "747270", 2: 3.0, 3: 2342.0},
{0: "1174587", 2: 4.0, 3: 2343.0},
{0: "1075528", 2: 4.0, 3: 2344.0},
{0: "1041042", 2: 3.0, 3: 2348.0},
{0: "1120573", 2: 4.0, 3: 2349.0},
{0: "1622639", 2: 4.0, 3: 2349.0},
{0: "1763559", 2: 3.0, 3: 2352.0},
{0: "437111", 2: 4.0, 3: 2363.0},
{0: "2097976", 2: 4.0, 3: 2363.0},
{0: "649662", 2: 3.0, 3: 2369.0},
{0: "2638072", 2: 4.0, 3: 2370.0},
{0: "694027", 2: 4.0, 3: 2374.0},
{0: "496408", 2: 4.0, 3: 2374.0},
{0: "426220", 2: 4.0, 3: 2377.0},
{0: "772936", 2: 4.0, 3: 2377.0},
{0: "1106511", 2: 4.0, 3: 2378.0},
{0: "981937", 2: 3.0, 3: 2380.0},
{0: "2419751", 2: 4.0, 3: 2384.0},
{0: "1818865", 2: 4.0, 3: 2392.0},
{0: "1150614", 2: 3.0, 3: 2393.0},
{0: "983833", 2: 4.0, 3: 2393.0},
{0: "2532368", 2: 4.0, 3: 2395.0},
{0: "1293557", 2: 4.0, 3: 2397.0},
{0: "1297965", 2: "4.0", 3: 2398.0}
]

#count_movie = ct(entry[3] for entry in records_test)
count_movie = ct(entry[3] for entry in nf_df_dict)

nf_df.set_index([3],inplace=True) # setze movieID als index also haupterkennung
ml_df.set_index([1],inplace=True) # setze movieID als index also haupterkennung
com_movies = nf_df.index.unique().intersection(ml_df.index.unique()) # gib nur die MovieIDs die beide haben

list_ecc, match_true, match_false = algorithm_1b(com_movies, count_movie, ml_df, nf_df, dummy_entries)

print(match_true)
print(np.mean(list_ecc))
#list_ecc, match_true, match_false = algorithm_1b(com_movies, count_movie, ml_df, nf_df)

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


create_histogram(list_ecc)





