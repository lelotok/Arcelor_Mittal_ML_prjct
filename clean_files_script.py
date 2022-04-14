import pandas as pd
import os

## go through files in coil_data, get their respective file and delete it

with open("../Metal_stuff/CoilData.csv") as file:
    df = pd.read_csv(file)

bad_files = os.listdir("../Metal_stuff/SignalExport")


files = os.listdir("../Metal_stuff/coil_data")

coils = []
for coil in df.coil:
    if f"{coil}B4.csv" not in files or f"{coil}B5.csv" not in files:
        coils.append(coil)
        print(coil)

print(len(coils))
