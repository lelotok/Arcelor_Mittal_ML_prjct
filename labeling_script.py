import pandas as pd
import numpy as np
from utils import filepaths

# Opening the files
df = pd.read_csv(filepaths.PATH_TO_BASE_CSV)
coil_list = df.coil

for coil in coil_list:

    B4 = pd.read_csv(f"{filepaths.PATH_TO_NEW}{coil}B4.csv")
    B5 = pd.read_csv(f"{filepaths.PATH_TO_NEW}{coil}B5.csv")

    # Splitting the Values columns, *change in script?*

    B4.rename(columns = {'Values':'B4_Values'}, inplace = True)
    B5.rename(columns = {'Values':'B5_Values'}, inplace = True)

    # Setting the desired Lengthpoints

    B4 = B4[B4.Lengthpoints >= 140]
    B5 = B5[B5.Lengthpoints >= 140]

    B4 = B4[B4.Lengthpoints <= 170]
    B5 = B5[B5.Lengthpoints <= 170]

    # Finding closest values from B5 Lengthpoints to B4 Lengthpoints.
    # This will then change the Lengthpoint of B5 to the closest matching B4 Lengthpoint.

    index = 0
    B4_array = B4['Lengthpoints'].to_numpy()
    B5_array = B5['Lengthpoints'].to_numpy()

    for lengthpoint in B5.Lengthpoints:

        closest = np.abs(B4_array-lengthpoint).argmin()
        smallest_difference_index = closest.argmin()
        closest_element = B4_array[smallest_difference_index]

        B5_array[index] = closest_element
        index+=1

    B5.Lengthpoints = B5_array

    # Creating a merged dataframe of B4 and B5.
    # Adding a difference column to show all width differences in mm.
    # Filling the NaN values with the next value or if not available the previous value.

    # If you don't want any NaN values in the dataframe, you can remove the 'how= 'left''
    # from merged_df = pd.merge(B4,B5, how= 'left'). This will then automatically exclude the NaN values.

    merged_df = pd.merge(B4,B5, how= 'left')
    merged_df['difference'] = merged_df['B5_Values']-merged_df['B4_Values']
    merged_df.fillna(method ='bfill', inplace = True)
    merged_df.fillna(method ='pad', inplace = True)

    # We create the values to put into the columns of CoilData

    possible_constriction_count = (merged_df['difference']<=-4).sum()

    diff = merged_df['difference'].min()

    constrictions = []
    for each in merged_df['difference']:
        if each <= -4:
            constrictions.append(each)

    # We write the information to out CoilData file so we have an overview of which one constricted, what the largest constriction
    # is per coil and how many constrictions of equal to or over 4mm there are.

    coil_index = df.index[df['coil'] == coil].tolist()

    if len(constrictions) == len(merged_df.difference):
        df.at[coil_index[0],'Constriction'] = "False"
    elif diff <= -4:
        df.at[coil_index[0],'Constriction'] = "True"
        df.at[coil_index[0],'Max separation'] = abs(diff)
        df.at[coil_index[0],'Number of separation points'] = possible_constriction_count
    else:
        df.at[coil_index[0],'Constriction'] = "False"

df.to_csv(filepaths.PATH_TO_LABELED_CSV, index=False)
