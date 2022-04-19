import pandas as pd


def file_range_access(
    x_range,
    y_range=0,
    folder_path="../Metal_stuff/coil_data/",
    file_path="../Metal_stuff/CoilData.csv",
):

    x_range, y_range = (x_range, y_range) if x_range < y_range else (y_range, x_range)

    with open(file_path) as file:
        df = pd.read_csv(file)

    coils = df.coil[x_range:y_range]

    return coils
