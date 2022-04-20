import re
import os
import pandas as pd
import numpy as np

PATH_TO_OLD = "../SignalExport/"
PATH_TO_NEW = "../Cleaned_data/"
PATH_TO_CSV = "../CoilData.csv"

with open(PATH_TO_CSV) as coil_csv:
    coil_df = pd.read_csv(coil_csv, sep=";")

bad_coils = []

for coil in coil_df.coil:
    for index in ["4", "5"]:
        try:
            with open(f"{PATH_TO_OLD}{coil}B{index}.csv") as read_file:
                file_content = read_file.read()

            ## This regex will extract the data from the files in 2 capture groups
            captures = re.search(r'.*Lengthpoints:;(.*)Values;(.*)', file_content)

            ## If nothing gets captured, the file will be skipped
            if captures != None:
                lengthpoints = captures.group(1)
                values = captures.group(2)

                lengthpoints = lengthpoints.split(";")
                values = values.split(";")

                ## This both cleans the data and puts it in an iterable array
                clean_data = [(lengthpoint, value) for (lengthpoint, value) in zip(lengthpoints, values) if lengthpoint != '0' and lengthpoint != "" and value != '0' and value != ""]

                if len(clean_data) == 0:
                    bad_coils.append(coil)
                    break

                ## This is once again a relative path and needs to be edited to point
                ## to the correct directory
                with open(f"{PATH_TO_NEW}{coil}B{index}.csv", "w") as write_file:

                    ## Now we write the data to new csv and delete the old file, this
                    ## will lead to us having all cleaned and correct files in the
                    ## directory and leave any faulty files in the old directory, we can
                    ## now iterate over those files and try to remove them if necessary
                    write_file.write("Lengthpoints,Values\n")
                    write_file.writelines(lengthpoint + "," + value + "\n" for (lengthpoint, value) in clean_data)

                    os.remove(f"{PATH_TO_OLD}{coil}B{index}.csv")

            else:
                bad_coils.append(coil)
                break

        except FileNotFoundError:
            bad_coils.append(coil)
            break

final_coils = os.listdir(PATH_TO_NEW)


for coil in bad_coils:
    if f"{coil}B4.csv" in final_coils:
        os.remove(f"{PATH_TO_NEW}{coil}B4.csv")

coil_df = coil_df[coil_df.coil.isin(bad_coils) == False]

coil_df.to_csv("../CoilData_new.csv")

print(f"Done! {len(bad_coils)} coils removed")
