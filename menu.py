# -*- coding: utf-8 -*-
"""
Created on Thu Januar 14 17:31:18 2023

@author:Jawwad Khan,7417247,Thesis Cybersecurity,Title: The Role of the Adversary's Success Rate Metric in Cybersecurity
"""


import preprocessing.preprocessing as preprocess
import preprocessing.normalizetime as nt

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


def option3():
    print("You selected Option 3")
    preprocess.complete_process()
    nt.normalize_time()

def start_menu():
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