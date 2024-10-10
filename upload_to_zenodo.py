import os
import shutil
import pandas as pd

year = "2040"
root = "//ad.geo.uu.nl/Users/StaffUsers/6574114/EhubResults/MES NorthSea/2040_demand_v6_simplifiedgrids"
results = pd.read_csv("./data/Summary_"+year+".csv", sep=";")
destination_dir = ("//ad.geo.uu.nl/Users/StaffUsers/6574114/EhubResults/MES "
                   "NorthSea/00_FinalResults")
for index, row in results.iterrows():
    folder = row['file']
    case_name = row['Case']
    subcase_name = row['Subcase']
    objective =  row['objective']

    # Construct the source file path
    source_file_path = os.path.join(root, folder, 'optimization_results.h5')

    # Construct the new file name using Case and Subcase
    new_file_name = f"{year}_{objective}_{case_name}_{subcase_name}.h5"

    # Construct the full destination file path
    destination_file_path = os.path.join(destination_dir, new_file_name)

    # Check if the source file exists before copying
    if os.path.exists(source_file_path):
        # Copy the file to the destination directory with a new name
        shutil.copy(source_file_path, destination_file_path)
        print(f"Copied to {destination_file_path}")
    else:
        print(f"File {source_file_path} does not exist")