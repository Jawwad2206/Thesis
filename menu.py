# -*- coding: utf-8 -*-
"""
Created on Thu Januar 14 17:31:18 2023

@author: Jawwad Khan, 7417247, Thesis Cybersecurity, Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""

import pandas as pd

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
    # nrows=10 bedeutet die ersten 10 reihen nur lesen
    df = pd.read_csv("DF.csv", encoding="UTF-8", sep=";")
    db = pd.read_csv("DB.csv", encoding="UTF-8", sep=";")

    print(db.head(), "db.head")
    print(len(db), "db")
    print(len(db.userId.unique()))

    print("___________________________________________")

    print(df.head(), "df.head")
    print(len(df), "df")
    print(len(df.userId.unique()), "df")

    # Count the number of NaN values in each row
    nan_counts_per_row = df.isna().sum(axis=1)

    # Count the total number of rows with NaN values
    total_rows_with_nan = nan_counts_per_row.sum()

    # Display the result
    print(f"Total number of rows with NaN values: {total_rows_with_nan}")

    df = df.dropna()

    print(df.head())

    # Count the number of NaN values in each row
    nan_counts_per_rowss = df.isna().sum(axis=1)

    # Count the total number of rows with NaN values
    total_rows_with_nanss = nan_counts_per_rowss.sum()

    # Display the result
    print(f"Total number of rows with NaN values: {total_rows_with_nanss}")


def option2():
    print("You selected Option 2")


def option3():
    print("You selected Option 3")
    dh_ad.complete()


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