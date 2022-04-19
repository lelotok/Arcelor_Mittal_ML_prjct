import pandas as pd
from utils import filepaths

def file_range_access(
    x_range,
    y_range=0,
    folder_path=filepaths.PATH_TO_NEW,
    file_path=filepaths.PATH_TO_BASE_CSV,
):

    x_range, y_range = (x_range, y_range) if x_range < y_range else (y_range, x_range)

    with open(file_path) as file:
        df = pd.read_csv(file)

    coils = df.coil[x_range:y_range]

    return coils
