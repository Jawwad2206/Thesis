# -*- coding: utf-8 -*-
"""
Created on Thu January 14 17:31:18 2023

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity

The code is based on the information provided by the paper: https://systems.cs.columbia.edu/private-systems-class/papers/Narayanan2008Robust.pdf
The authors did not provide a link to their personal GitHub Repository and only described their code through written
text. The following implementation is my interpretation and understanding of their written text. A more thorough
explanation can be found in my bachelor thesis in Chapter 4.
"""

import pandas
import pandas as pd
import numpy as np
from collections import Counter as ct
import matplotlib.pyplot as plt


def sim(rating, timestamp, aux_rating, aux_timestamp):
    """
    Calculate the similarity score between two items based on their timestamps and ratings.

    Args:
        timestamp (float): Timestamp of the record in Netflix.
        aux_timestamp (float): Timestamp of the auxiliary record in MovieLens.
        rating (float): Rating of the record in Netflix.
        aux_rating (float): Rating of the auxiliary record in MovieLens.

    Returns:
        float: Similarity score between the two items.

    The similarity score is calculated based on the difference in timestamps and ratings between two records.
    A higher score indicates greater similarity.

    - If the absolute difference in timestamps is less than or equal to 14:
        - If the absolute difference in timestamps is less than or equal to 3, add 1 to the similarity score.
        - Otherwise, do not modify the similarity score.
    - If the difference in ratings is 0, add 1 to the similarity score.
    - If both the timestamp and rating differences are 0, add 10 to the similarity score.

    """

    sim_score = 0

    # Check if the absolute difference in timestamps is less than or equal to 14
    if abs(aux_timestamp - timestamp) <= 14:
        # If the absolute difference in timestamps is less than or equal to 3, add 1 to the similarity score
        if abs(aux_timestamp - timestamp) <= 3:
            sim_score += 1
        else:
            sim_score += 0
    else:
        sim_score += 0

    # Check if the difference in ratings is 0
    if abs(rating - aux_rating) == 0:
        sim_score += 1
    else:
        sim_score += 0

    # Check if both the timestamp and rating differences are 0
    if (aux_timestamp - timestamp) == 0 and (aux_rating - rating) == 0:
        sim_score += 10

    return sim_score

def score_function(aux, record, counts):
    """
        Calculate a combined score based on rating, timestamp, and similarity between two records.

        Args:
            aux (dict): Auxiliary record containing rating and timestamp information.
            record (dict): Current record containing rating and timestamp information.
            counts (int): Count of records.

        Returns:
            float: Combined score based on rating, timestamp, and similarity.

        The combined score is calculated using a weighted sum of similarity score and a score function of
        rating and timestamp differences between two records.

        - If the auxiliary timestamp is negative, return 0.
        - Otherwise, calculate the similarity score between the current and auxiliary records.
        - Calculate the weight (wt) based on the logarithm of the count of records.
        - Compute the combined score using the weighted sum of the similarity score and the decay function
          of rating and timestamp differences.
        """
    sim_score = 0
    score = 0

    #parameter for rating
    rho0 = 1.5
    #parameter for timestamp
    d0 = 30
    rating = float(record.get(1))
    timestamp = float(record.get(2))
    aux_rating = float(aux.get(2))
    aux_timestamp = float(aux.get(3))

    if aux_timestamp < 0:
        score = 0
    else:
        # Calculate the similarity score between the current and auxiliary records
        sim_score = sim(rating, timestamp, aux_rating, aux_timestamp)

        # Calculate the weight (wt) based on the logarithm of the count of movies in the Netflix dataset
        wt = (1/(np.log10(counts)))

        # Compute the combined score using the weighted sum of the similarity score and the decay function
        score = wt * (np.exp(-((aux_rating - rating)) / rho0) + np.exp((-aux_timestamp - timestamp) / d0))

    return score + sim_score

def matching_criterion(scores, eccentricity):
    """
       Determine if there is a match based on scores and eccentricity threshold.

       Args:
           scores (list of float): List of scores.
           eccentricity (float): Eccentricity threshold.

       Returns:
           tuple: A tuple containing three elements:
               - bool: Indicates whether there is a match.
               - float: Maximum score in the list.
               - float: Calculated eccentricity value.

       The function checks if there is a match based on the scores and a specified eccentricity threshold.
       If the sum of scores is 0, it returns False along with the maximum score and calculated eccentricity.
       If there is only one score in the list, it returns False if the score is less than 2, otherwise, it returns True,
       along with the maximum score and calculated eccentricity.
       Otherwise, it sorts the scores in descending order, removes duplicates, calculates the maximum score and the
       second maximum score, computes the standard deviation (sigma) of the scores, calculates the eccentricity based on
       the maximum and second maximum scores and the sigma value, and finally determines if there is a match based on
       the calculated eccentricity and the specified eccentricity threshold.
       """

    if (sum(scores) == 0):
        return False, 0, 0
    elif len(scores) == 1:
        max_score = scores[0]
        if max_score < 2:
            return False, max_score, max_score
        else:
            return False, max_score, max_score
    else:
        # Sort the scores in descending order
        sorted_scores = sorted(scores, reverse=True)
        # Remove duplicates and maintain the order
        unique_list = list(sorted(set(sorted_scores), reverse=True))
        # Find the maximum and second maximum scores
        max_score = unique_list[0]
        max2_score = unique_list[1]
        # Calculate the standard deviation of scores
        sigma = np.std(scores)
        # Calculate eccentricity
        ecc_calc = ((max_score - max2_score) / sigma)
        # Check if there is a match based on the calculated eccentricity and the specified eccentricity threshold
        if ecc_calc < eccentricity:
            return False, max_score, ecc_calc
        else:
            return True, max_score, ecc_calc

def record_selection(scores):
    """
        Select a record index based on scores using probability distribution.

        Args:
            scores (list of float): List of scores.

        Returns:
            Union[int, dict]: If there is only one score in the list, returns that score.
            Otherwise, returns a dictionary representing the probability distribution of record indices.

        The function selects a record index based on scores using a probability distribution.
        If there is only one score in the list, it returns that score.
        Otherwise, it calculates the probability distribution for each score based on the exponential of the score
        divided by the standard deviation of scores, then returns a dictionary representing the probability distribution
        of record indices, where each key represents a record index and each value represents the probability of
        selecting that record.
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
        Implement algorithm 1b of the paper: https://systems.cs.columbia.edu/private-systems-class/papers/Narayanan2008Robust.pdf

        Args:
            com_movie (list): List of common movie IDs between Netflix and MovieLens.
            counts_movie (dict): Dictionary containing counts of movies for each movie in Netflix.
            ml_df (pandas.DataFrame): DataFrame containing auxiliary information for movies (MovieLens).
            nf_df (pandas.DataFrame): DataFrame containing records for movies (Netflix).

        Returns:
            tuple: A tuple containing three elements:
                - list: List of eccentricities for matched records.
                - int: Count of matches.
                - int: Count of mismatches.

        The function implements algorithm 1b. It iterates through each movie ID in com_movie.
        For each movie, it retrieves records and auxiliary information from corresponding DataFrames.
        It then calculates scores and determines matches based on a specified eccentricity threshold.
        The function prints information about each record and match.
        It returns a tuple containing a list of eccentricities for matched records, the count of matches, and the count
        of mismatches.
        """
    eccentricity = 1.5
    # List to store eccentricities for matched records
    list_ecc = []
    # Counter for matches
    match_true = 0
    # Counter for mismatches
    match_false = 0

    # Iterate through each movie ID
    for id in com_movie:
        aux_list_one = []
        # Retrieve records for the current movie
        records_i = nf_df.loc[id,:]
        # Retrieve auxiliary information for the current movie
        auxiliary_information_i = ml_df.loc[id,:]
        # Convert records DataFrame to a list of dictionaries
        records = records_i.to_dict("records")
        # If the auxiliary information is a Series, convert it to a dictionary and append it to a list
        if isinstance(auxiliary_information_i, pandas.Series):
            auxiliary_information = auxiliary_information_i.to_dict()
            aux_list_one.append(auxiliary_information)
            auxiliary_information = aux_list_one
        else:
            # Convert auxiliary info to list of dicts
            auxiliary_information = auxiliary_information_i.to_dict("records")
        # Iterate through each record of the current movie
        for record in records:
            # List to store scores for each auxiliary record
            scores = []
            print("MovieID:", id, "Record ->", record)
            # Calculate score for each auxiliary record
            for aux in auxiliary_information:
                score = score_function(aux, record, counts_movie.get(id))
                scores.append(score)
            # Determine if there is a match based on the scores and eccentricity threshold
            match, max_score, ecc = matching_criterion(scores, eccentricity)
            print("------------------------------------------")
            if match == True:
                match_true +=1
                if max_score == ecc:
                    continue
                else:
                    # Store eccentricity for matched records
                    list_ecc.append(ecc)
                pd = record_selection(scores)
                # Print information about each record and match
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


def start_algorithm_1B():
    """
        Start the execution of algorithm 1B.

        This function loads the Netflix (nf.csv) and MovieLens (ml.csv) datasets, performs necessary preprocessing,
        calculates counts of records for each movie in the Netflix dataset, identifies common movie IDs between
        Netflix and MovieLens datasets, and executes algorithm 1B for the common movies.

        Returns:
            list: A list containing eccentricities for matched records.

        Algorithm 1B compares records from the Netflix and MovieLens datasets to find matches based on similarity
        scores and a specified eccentricity threshold. It iterates through common movie IDs, calculates similarity
        scores for each record pair, determines matches, and prints information about the matches. The function returns
        a list of eccentricities for matched records.

        Note: Paths to the datasets are hard-coded and need to be adjusted based on the actual file locations.
        """
    # Load nf.csv and ml.csv datasets
    nf_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA"
                        "\\BA-Implementierung\\datasets\\Netflix.csv",
                        header=None, encoding="UTF-8", sep=";", skiprows=1, nrows=100000)

    ml_df = pd.read_csv("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\"
                        "7.Semester\\BA\\BA-Implementierung\\datasets\\MovieLens.csv",
                        header=None, encoding="UTF-8", sep=";", skiprows=1, nrows=100000)

    # original length of entry -> 76024778
    nf_df_dict = nf_df.to_dict("records")

    # original length of entry -> 13661758
    #ml_df_dict = ml_df.to_dict("records")

    # Calculate counts of movies for each movie in Netflix dataset
    count_movie = ct(entry[3] for entry in nf_df_dict)

    # Set movieID as index for both DataFrames
    nf_df.set_index([3], inplace=True)
    ml_df.set_index([1], inplace=True)

    # Get common movie IDs between Netflix and MovieLens datasets
    com_movies = nf_df.index.unique().intersection(ml_df.index.unique())

    # Execute algorithm 1b for the common movies
    list_ecc, match_true, match_false = algorithm_1b(com_movies, count_movie, ml_df, nf_df)

    return list_ecc


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










