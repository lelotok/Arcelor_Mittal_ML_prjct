# Project for ArcelorMittal: Predicting width constrictions during hot rolling.
### [Bertram D'Hooghe](https://github.com/BertramDHooge), [Lelo Tokwaulu](https://github.com/lelotok) and [Kristof Vandewynckel](https://github.com/KristofVandewynckel)
--------------------------------------------------------------------------------------

## Introduction

We are three students at BeCode Ghent, training to become Junior Data Scientists/ AI Operators. At the time of this project we were two months into the training and had just finished some basic Machine Learning models. This project was given to our class by ArcelorMittal to expand upon our training and provide a possible solution to their problem.

## Description

The goal of this project is to create a Machine Learning model to predict possible width constrictions on coils. In the production of their metal coils, there's a moment when the steel plate is grabbed by the coiler which spins the steel plate into a roll. This moment has sometimes created a constriction in the width of the steel plate. This usually happens between 140 and 170 metres. 

With our model, we want to predict before a steel slab starts the production process, if it's probable that it'll have a width constriction or not.

## Modules used

- Python
- Pandas
- Numpy
- Sklearn

## Installation

1. Clone the repo
2. Install the libraries

## Step 0: Set filepaths

Before starting the scripts or trying the models, make sure your filepaths are correct. Use the [filepath.py](https://github.com/lelotok/Arcelor_Mittal_ML_prjct/blob/main/labeling_script.py) and follow the steps inside.

## Step 1: Exploring data.

For this we were given several .csv files. One was an overview of all the coils (CoilData) and several parameters such as Width, material composition, temperature, hardness,...
The others were specifc measurements of each coil. At about every 30 cm a measurement of the Width was made, this happened at two measuring points in the production process. One called B4, the other B5. The difference between these two shows us when width constriction happens.

## Step 2: Preparing the data.

Our first step was to make the data usable, the way it was stored in the .csv made immediate usage impossible and it needed to be rearranged. For this we created the [csv_cleaning_script.py.](https://github.com/lelotok/Arcelor_Mittal_ML_prjct/blob/main/csv_cleaning_script.py) . This script loops over all the coils in the CoilData .csv , arranges all the data so it's immediately readable for a Pandas DataFrame. It furthermore removed any files that did not have a B4 or B5 counterpart and checked if it was present in the CoilData overview. It also looked at the values inside the coil file and if they were faulty (eg. all zeroes, a width of 1mm,...) they were also removed.

## Step 3: Labeling the data.

After step 2 we were left with over 50.000 files all with B4 and B5 measurements. Now we had to correctly identify what coils had had a width constriction and which hadn't. To do this we ran the [labeling.py](https://github.com/lelotok/Arcelor_Mittal_ML_prjct/blob/main/labeling_script.py) . This file loops over the CoilData.csv and opens the specific coil B4 & B5 files. It then looks at only the data between 140 and 170 metres, as requested by the client. Since the measuring points aren't at the same lengthpoint for B4 and B5 we try to find the closest matching value for B5. This way we can create a dataframe which compares the width differences between B4 & B5.

The script then adds columns to the original CoilData.csv and labels, depending on parameters, whether a coil has had a constriction (True) or not (False). 

## Step 4: Testing models

After labeling the data to True and False, we started testing several models. These can be found [here](https://github.com/lelotok/Arcelor_Mittal_ML_prjct). The models gave back different results and you can try them out for yourself. The models that gave the most satisfactory result for us were #1 SVC and #2 SGDClassifier. Be warned that SVC runs quite slow but gives a more accurate result.
