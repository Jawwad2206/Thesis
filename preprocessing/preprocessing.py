# -*- coding: utf-8 -*-
"""
Created on Thu January 11 16:51:18 2024

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity

This code is based on the code of BigBrother

Source :https://github.com/mpetitjean/BigBrother/blob/master/src/clean_ML_db.ipynb
(Accessed: Thu January 11 16:51:18 2024)

The code had to be adjusted because of old dependencies and use case.
"""

import pandas as pd
import preprocessing.datasets as ld
from datetime import datetime
import csv


def data_cleanup(db):
    """
    This code is based on the code of BigBrother

    Source :https://github.com/mpetitjean/BigBrother/blob/master/src/clean_ML_db.ipynb
    (Accessed: Thu January 11 16:51:18 2024)

    The code had to be adjusted because of old dependencies and use case.

    Clean up the movie ratings of the MovieLens database by removing out-of-bounds entries based on timestamp and
    extracting a list of distinct movieIds for further processing.

    Parameters:
    - db (pd.DataFrame): MovieLens database.

    Returns:
    - list_ml_movies (numpy.ndarray): Array of distinct movieIds.
    """
    print("Starting Cleanup [1/3]")

    # Create the start and stop boundaries for the timestamp
    start_date = datetime(1998, 10, 1).timestamp()
    end_date = datetime(2006, 1, 1).timestamp()

    # Identify out-of-bounds entries
    a = (db["timestamp"] < start_date)
    print("There are", sum(a), "reviews made before the 1st October 1998.")
    b = (db["timestamp"] > end_date)
    print("There are", sum(b), "reviews made after the 31st December 2005.")
    print("Number of NaN values in timestamp column:", db["timestamp"].isna().sum())

    # Remove out-of-bounds entries
    db = db[~a & ~b]

    # Display the first few rows of the modified database
    db.head()

    # Get number of distinct users
    list_ml_movies = db.movieId.unique()
    print("There are", len(db.userId.unique()), "users left.")
    print("There are", len(db.movieId.unique()), "movies left.")


    return list_ml_movies


def merge_movie_datasets(list_ml_movies):
    """
    This code is based on the code of BigBrother

    Source :https://github.com/mpetitjean/BigBrother/blob/master/src/clean_ML_db.ipynb
    (Accessed: Thu January 11 16:51:18 2024)

    The code had to be adjusted because of old dependencies and use case.

    Merge movie datasets from Netflix and MovieLens, filtering out problematic movie titles.

    Parameters:
    - list_ml_movies (numpy.ndarray): Array of distinct movieIds from MovieLens.

    Returns:
    - nf_movies (pd.Series): Netflix movie data.
    - ml_movies (pd.Series): MovieLens movie data.
    """
    print("Starting movie filter [2/3]")

    # List of problematic movie titles that cannot be uniquely identified
    wrong_movies = ["pinocchio(2002)", "lastmanstanding(1996)", "emma(1996)",
                    "hamlet(2000)", "hamlet(1990)", "menwithguns(1997)",
                    "thehunchbackofnotredame(1999)", "thelucyshow(1962)",
                    "stranded(2002)", "frankenstein(2004)", "secondskin(2000)",
                    "elvira'shorrorclassics(1959)", "waroftheworlds(2005)",
                    "chaos(2005)", "offside(2006)", "blackout(2007)", "thegirl(2012)",
                    "crimewave(1985)", "20,000leaguesunderthesea(1997)",
                    "aladdin(1992)", "beneath(2013)", "thedisappeared(2008)",
                    "paradise(2013)", "clearhistory(2013)", "casanova(2005)",
                    "johnnyexpress(2014)", "darling(2007)"]

    # Initialize an empty dictionary to store Netflix movie data
    nf_movies = {};
    # Open the movie_titles.txt file from the Netflix Prize dataset using a CSV reader
    with open("datasets\\nf_prize_dataset\\download\\movie_titles.txt", encoding="ISO-8859-1") as nf:

        # Iterate through each line in the CSV file
        for col1, col2, *col3 in csv.reader(nf):

            # Concatenate the title, release year, and additional information (if any)
            s = (''.join(col3) + "(" + col2 + ")").lower().replace(" ", "")

            # Check if the concatenated title is not in the list of problematic movie titles
            if s not in wrong_movies:

                # Assign the movie ID (col1) to the concatenated title in the dictionary
                nf_movies[s] = int(col1)

    # Convert the dictionary nf_movies into a pandas Series, naming it 'Netflix'
    nf_movies = pd.Series(nf_movies, name='Netflix')

    # Initialize an empty dictionary to store MovieLens movie data
    ml_movies = {};

    # Open the movies.csv file from the MovieLens dataset using a CSV reader
    with open("datasets\\ml-20m\\movies.csv", encoding="UTF-8") as ml:

        # Create a CSV reader for the file
        ml_reader = csv.reader(ml)

        # Skip the header row
        next(ml_reader)

        # Iterate through each line in the CSV file
        for col1, col2, *col3 in csv.reader(ml):

            # Check if the movie ID (col1) is in the list of distinct movie IDs from MovieLens
            if int(col1) in list_ml_movies:

                # Concatenate the movie title, convert to lowercase, and remove spaces
                s = ''.join(col2).lower().replace(" ", "")

                # Check for specific prefixes in the title and modify accordingly
                loc = s.find(",the(")
                if loc != -1:
                    s = "the" + s[:loc] + s[loc + 4:]
                else:
                    loc = s.find(",a(")
                    if loc != -1:
                        s = "a" + s[:loc] + s[loc + 2:]
                    else:
                        loc = s.find(",an(")
                        if loc != -1:
                            s = "an" + s[:loc] + s[loc + 3:]

                # Check if the modified title is not in the list of problematic movie titles
                if s not in wrong_movies:

                # Add an entry to the ml_movies dictionary with the modified title as the key and movie ID as the value
                    ml_movies[s] = int(col1)

    # Convert the dictionary ml_movies into a pandas Series, naming it 'MovieLens'
    ml_movies = pd.Series(ml_movies, name='MovieLens')

    return nf_movies, ml_movies


def intersection_of_movie(nf_movies, ml_movies, db):
    """
    This code is based on the code of BigBrother

    Source :https://github.com/mpetitjean/BigBrother/blob/master/src/clean_ML_db.ipynb
    (Accessed: Thu January 11 16:51:18 2024)

    The code had to be adjusted because of old dependencies and use case.

    Identify the intersection of movies between Netflix and MovieLens datasets and prepare the final datasets.

    Parameters:
    - nf_movies (pd.Series): Netflix movie data.
    - ml_movies (pd.Series): MovieLens movie data.
    - db (pd.DataFrame): original MovieLens dataset.

    """
    print("Starting the intersection of movies process [3/3]")

    # Find intersection of movie lists using title+date
    common_movies = nf_movies.index.intersection(ml_movies.index)

    # Create a Series 'matches' with MovieLens movie IDs as data and Netflix movie IDs as index
    matches = pd.Series(data=ml_movies.loc[common_movies].values, index=nf_movies.loc[common_movies].values)
    matches.name = 'ml_movieId'
    matches.index.name = 'nf_movieId'

    # Print the number of matches
    print('There is', matches.shape[0], 'matches')
    print("Preparing Movielens dataset, it can take a moment..")

    # Discard non-matches from the original database
    db = db.loc[db['movieId'].isin(matches), :]
    print("Process finish, creating ml.csv. Pls wait a moment...")

    # Initialize an empty list 'z' for Netflix dataset preparation
    z = []
    print("Preparing Netflix dataset, it can take a moment..")
    print("[______________]")

    # Iterate through the matched movie IDs
    for i in matches.index:

        # Read Netflix dataset corresponding to the matched movie ID
        tmp = pd.read_csv(
            "datasets\\nf_prize_dataset\\download\\training_set\\training_set\\mv_" + format(i, '07d') +
            ".txt", header=None, names=["userId", "rating", "timestamp"], encoding="ISO-8859-1")

        # Add a 'movieId' column to the Netflix dataset with the corresponding MovieLens movie ID
        tmp["movieId"] = matches[i]

        # Append the modified Netflix dataset to the list
        z.append(tmp)

    # Concatenate the list of Netflix datasets into a single dataframe 'df'
    df = pd.concat(z, copy=False)

    # Sanity check: Ensure the number of unique movie IDs in MovieLens, Netflix, and matches are equal
    assert db.movieId.unique().shape[0] == df.movieId.unique().shape[0] == matches.shape[0]

    # Save the Netflix and MovieLens datasets to CSV files
    df.to_csv("datasets\\nf.csv", ";", index=False)
    db.to_csv("datasets\\ml.csv", ";", index=False)


def complete_process():
    """
    Perform the complete process of cleaning up data, merging datasets, and identifying the intersection of movies.
    """
    db = ld.load_training_ml()
    list_movie_ml = data_cleanup(db)
    nf_movies, ml_movies = merge_movie_datasets(list_movie_ml)
    intersection_of_movie(nf_movies, ml_movies, db)

