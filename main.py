# -*- coding: utf-8 -*-
"""
Created on Thu Decemeber 14 17:31:18 2023

@author: Jawwad Khan, 7417247, Thesis Cybersecurity, Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import pandas as pd
import numpy as np
import datapreprocessing.pre_processing_db as dh_ad
import datapreprocessing.normalizetime as normt


def show_welcome():
    print("*************************************")
    print("*  Welcome to my Bachelor Thesis  *")
    print("*  -      The Role of the         *")
    print("* Adversary's Success Rate Metric *")
    print("*        in Cybersecurity -       *")
    print("*************************************")

def show_menu():
    print("\n1. General Information")
    print("2. Start")
    print("3. test")
    print("4. Exit")

def option1():
    print("You selected Option 1")


def option2():
    print("You selected Option 2")
    normt.normalize_time()

def option3():
    print("You selected Option 3")
    ml_db = dh_ad.load_training_ml()
    list_ml_movies = dh_ad.adjust_timestemps(ml_db)
    ml_movies, nf_movies = dh_ad.remove_not_matching(list_ml_movies)
    dh_ad.intersection_movies(ml_db, ml_movies, nf_movies)

show_welcome()
while True:
    show_menu()
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        option1()
    elif choice == '2':
        option2()
    elif choice == '3':
        option3()
    elif choice == '4':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")