import os

import pandas as pd

statistical_data_files = ["aktie", "leistungsdaten", "umsatz_ergebnis", "aggregate"]
input_directory = "data/"

for file in statistical_data_files:
    complete_input_file_path = input_directory + file + ".xlsx"
    read_file = pd.read_excel(complete_input_file_path)
    complete_output_file_path = input_directory + file + ".csv"
    read_file.to_csv(complete_output_file_path, index=None, header=True)

