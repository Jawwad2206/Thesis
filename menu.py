# -*- coding: utf-8 -*-
"""
Created on Thu January 14 17:31:18 2023

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity

This is the menu of this program, there all available options and desired tasks can be started.
"""


import preprocessing.preprocessing as preprocess
import preprocessing.normalizetime as nt
import pandas as pd

def show_welcome():
    """
    Shows a welcome message one time
    """
    print("*************************************")
    print("*  Welcome to my Bachelor Thesis  *")
    print("*  -      The Role of the         *")
    print("* Adversary's Success Rate Metric *")
    print("*        in Cybersecurity -       *")
    print("*************************************")

def show_menu():
    """
    shows what number has to be pressed to start a certain module
    """
    print("\n1. Start Data Pre-Processing steps")
    print("2. Start the De-Anonymization Algorithm")
    print("3. test")
    print("4. Exit")

def option1():
    """
    starts option 1, which starts the data pre-processing steps. It is important to note, that this program requires
    datasets, which should be in the directory "datasets". Otherwise, the path to the datasets should be added to the
    lines.
    """
    print("You selected Option 1: Data Pre-Processing steps")
    preprocess.complete_process()
    nt.normalize_time()

def option2():
    """
    starts option 2, the main algorithm of the thesis.
    The de-anonymization is based on the example provided by Arvind Narayanan and Vitaly Shmatikov
    """
    print("You selected Option 2: De-Anonymization Algorithm")
    df = pd.read_csv("datasets\\MovieLens.csv",
                     header=None, encoding="UTF-8", sep = ";", nrows=10)


    db = pd.read_csv("datasets\\Netflix.csv",
                     header=None, encoding="UTF-8", sep = ";", nrows=10)

    print(db)

    print(df)

def option3():
    """
    starts option 3,

    """
    print("You selected Option 3")


def start_menu():
    """
    Display a welcome message, show a menu with options, and handle user input for menu options.

    Options:
    1. option1(): starts the data pre-processing steps.
    2. option2(): the main algorithm of the thesis.
    3. option3(): ....
    4. Exit the program.

    Returns:
    None
    """

    # Display a welcome message
    show_welcome()
    while True:
        # Display the menu options
        show_menu()

        # Get user input for the chosen option
        choice = input("Enter your choice (1-4): ")
        # Handle user choice

        if choice == '1':
            # Execute action for option 1
            option1()
        elif choice == '2':
            # Execute action for option 2
            option2()
        elif choice == '3':
            # Execute action for option 3
            option3()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            # Exit the loop and end the program
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")