# -*- coding: utf-8 -*-
"""
Created on Thu Januar 11 16:51:18 2024

@author: Jawwad Khan, 7417247, Thesis Cybersecurity, Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""
import pandas as pd
from datetime import datetime
import csv


def complete():
    db = pd.read_csv(
        "C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA\\ml-20m\\ml-20m\\ratings.csv",
        header=0, encoding="UTF-8", dtype={0: int, 1: int, 2: float, 3: float},
        names=["userId", "movieId", "rating", "timestamp"])

    print(len(db), "orginal")
    print(db.shape)

    print("Minimum Timestamp:", db["timestamp"].min())
    print("Maximum Timestamp:", db["timestamp"].max())

    print("There are", len(db.userId.unique()), "users left. -----")
    print("There are", len(db.movieId.unique()), "movies left. ----- ")

    # Create the start and stop boundaries for the timestamp
    # format: seconds elapsed since 1st Jan 1970
    start_date = datetime(1998, 10, 1).timestamp()
    end_date = datetime(2006, 1, 1).timestamp()

    # Remove out-of-bounds entries
    a = (db["timestamp"] < start_date)
    print("There are", sum(a), "reviews made before the 1st October 1998.")
    b = (db["timestamp"] > end_date)
    print("There are", sum(b), "reviews made after the 31st December 2005.")
    print("Number of NaN values in timestamp column:", db["timestamp"].isna().sum())

    db = db[~a & ~b]

    print(len(db), "after filter")

    db.head()
    # Get number of distincts users
    list_ml_movies = db.movieId.unique()
    print("There are", len(db.userId.unique()), "users left.")
    print("There are", len(db.movieId.unique()), "movies left.")



    # These titles are present several times and cannot be uniquely identified
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

    nf_movies = {};
    with open("C:\\Users\\jawwa\\Desktop\\nf_prize_dataset\\download\\movie_titles.txt", encoding="ISO-8859-1") as nf:
        for col1, col2, *col3 in csv.reader(nf):
            # s = ''.join(col3).lower().replace(" ","")
            # s = s[:(s.find('(') if s.find('(') !=-1 else len(s))]
            s = (''.join(col3) + "(" + col2 + ")").lower().replace(" ", "")
            if s not in wrong_movies:
                nf_movies[s] = int(col1)
    nf_movies = pd.Series(nf_movies, name='Netflix')

    ml_movies = {};
    with open("C:\\Users\\jawwa\\OneDrive\\Studium\\Goethe Universität - BA\\7.Semester\\BA\\ml-20m\\ml-20m\\movies.csv", encoding="UTF-8") as ml:
        ml_reader = csv.reader(ml)
        next(ml_reader)  # Skip the header row
        for col1, col2, *col3 in csv.reader(ml):
            if int(col1) in list_ml_movies:
                s = ''.join(col2).lower().replace(" ", "")
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
                if s not in wrong_movies:
                    ml_movies[s] = int(col1)

    ml_movies = pd.Series(ml_movies, name='MovieLens')
    print(len(nf_movies))
    print(len(ml_movies))
    # Find intersection of movie lists using title+date
    common_movies = nf_movies.index.intersection(ml_movies.index)
    matches = pd.Series(data=ml_movies.loc[common_movies].values, index=nf_movies.loc[common_movies].values)
    matches.name = 'ml_movieId'
    matches.index.name = 'nf_movieId'
    print('There is', matches.shape[0], 'matches')

    # Discard non matches
    db = db.loc[db['movieId'].isin(matches), :]
    z = []
    # df = pd.DataFrame(columns=["userId","movieId","rating","timestamp"])
    for i in matches.index:
        tmp = pd.read_csv("C:\\Users\\jawwa\\Desktop\\nf_prize_dataset\\download\\training_set\\training_set\\mv_" + format(i,'07d')+".txt", header=None, names=["userId","rating","timestamp"],encoding="ISO-8859-1")
        tmp["movieId"] = matches[i]
        z.append(tmp)
    df = pd.concat(z, copy=False)
    # Sanity check
    assert db.movieId.unique().shape[0] == df.movieId.unique().shape[0] == matches.shape[0]
    df.to_csv("DF.csv", ";", index=False)
    db.to_csv("DB.csv", ";", index=False)
