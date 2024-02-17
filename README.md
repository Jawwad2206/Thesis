# Thesis

Welcome to the practical component of my bachelor thesis project! 

This repository contains the code necessary to replicate and execute the experiments discussed in my thesis. 

Below are the steps to get started:


# Dataset Download Instructions
To proceed with running the experiments, you'll need to download two datasets: the Netflix dataset and the MovieLens dataset. 

Follow the instructions below to obtain and organize the datasets:

### Netflix Dataset:

Visit the following link to access the Netflix dataset: [Netflix Prize Data.](https://archive.org/download/nf_prize_dataset.tar)

Download the dataset "nf_prize_dataset.tar.gz" from the provided link. 

Once downloaded, extract the contents of the dataset archive to a folder on your local machine.

### MovieLens Dataset:

Go to the following link to access the MovieLens dataset: [MovieLens 20M Dataset.](https://grouplens.org/datasets/movielens/20m/)

Download the dataset from the provided link. This dataset is available for download without requiring registration.

After downloading, extract the contents of the dataset archive to a separate folder on your local machine.

### Organizing Datasets:

For convenience, let's create a folder named "datasets" to store both datasets:

Navigate to the directory where you downloaded the datasets.

Create a new folder named "datasets" if it doesn't already exist.

Move the extracted contents of both the Netflix dataset and the MovieLens dataset into the "datasets" folder.

Once you have completed these steps, you will have both datasets conveniently located in the "datasets" folder, ready for use in your experiments.

# Pre-execution Steps
Before executing the code, several pre-processing steps need to be completed. 

Follow the instructions below to ensure proper configuration:

* ### Update Dataset File Locations:
 1. Open the `datasets.py` file located in the preprocessing folder.
 2. Adjust the file locations within the functions according to your local directory structure.
* ### Set Netflix Dataset Location:
1. Open the `preprocessing.py` file located in the preprocessing folder.
2. Go to line 102 and insert the file location for the Netflix dataset movie_titles.txt.
3. Similarly, in line 123, insert the file location for the movies.csv from the MovieLens dataset.
4. Proceed to line 209 and insert the file location for the training set.

Important: When copying the path, modify it as follows: 

Change from "C:\...\...\...\...\...\...\...\...\datasets\nf_prize_dataset\download\training_set\training_set" to "C:\...\...\...\...\...\...\...\...\datasets\nf_prize_dataset\download\training_set\training_set\mv_". 

This adjustment ensures correct file concatenation during iteration.
* ### Create Datasets Folder:
If the datasets folder does not exist, create one. This folder will store the preprocessed datasets.

##  Deanonymization:
Navigate to the deanonymization folder and adjust the file locations in the following files:

#### `algorithm1b.py` and `algorithm1b_test.py`:
1. Open both `algorithm1b.py` and `algorithm1b_test.py`.
2. Go to line 304 and 308 in each file.
3. Adjust the file locations according to the location of the preprocessed Netflix dataset and MovieLens dataset.

These steps ensure that the code executes smoothly with the correct dataset locations and configurations.

# Code Execution Instructions

To execute the code for my Bachelor Thesis project, follow the steps below:

`*************************************`
*  Welcome to my Bachelor Thesis  *
*        The Role of the          *
* Adversary's Success Rate Metric *
*        in Cybersecurity         *
`*************************************`

1. Start Data Pre-Processing steps
2. Start the De-Anonymization Algorithm
3. Start the Dummy Test for the De-Anonymization Algorithm
4. Exit

Enter your choice (1-4):`

**IMPORTANT:** If you have not completed the preprocessing steps, select option 1 to initiate the data preprocessing. 

Ensure you have followed the pre-execution steps explained earlier. 
Once preprocessing is complete, you will return to this menu.

1. Selecting option 2 will start the De-Anonymization Algorithm. Please be patient as the algorithm may take some time to complete. During execution, outputs will be displayed in the console. Refer to the thesis for explanations of the displayed outputs. The algorithm is finished when the histogram displays on your screen.

2. Option 3 initiates the dummy test for the De-Anonymization Algorithm. This test provides insights into the algorithm's behavior under controlled conditions. Similar to option 2, please allow time for the test to complete, and refer to the thesis for further details.

3. Selecting option 4 exits the code execution.
# Literature
Arvind Narayanan and Vitaly Shmatikov, "Robust De-anonymization of Large Dataset (How to Break Anonymity of the Netflix Prize Dataset), 

2008, url: https://systems.cs.columbia.edu/private-systems-class/papers/Narayanan2008Robust.pdf.


# Disclaimer
In order to execute this code, you need to install the following dependencies:

* Numpy
* pandas
* matplotlib

These dependencies were executed in combination with Python 3.11 Compiler.


# Additional Notes:
* **_Contact:_** For more detailed information, please refer to the bachelor thesis or contact me via email at s2858054@stud.uni-frankfurt.de
* **_Feedback and Contributions:_** Feedback, suggestions, and contributions are highly appreciated! 
If you have any ideas for improvements or would like to contribute enhancements, please submit a pull request or open an issue on GitHub.