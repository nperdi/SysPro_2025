import os
import pandas as pd

# Directory where the downloaded files are stored

input_dir = "filtered_xls"
outputDir = "xls_concatenate"
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

output_file = os.path.join(outputDir, "concatenated.xlsx")

# List to store dataframes
all_dataframes = []

# Read each Excel file and append it to the list
for file in os.listdir(input_dir):
    if file.endswith(".xlsx") and file != "merged.xlsx":  # Ignore merged file if it exists
        file_path = os.path.join(input_dir, file)
        
        # Read the Excel file
        try:
            df = pd.read_excel(file_path, engine="openpyxl",header=None)
            df.insert(0, "Filename", file)  # Insert filename as the first column
            all_dataframes.append(df)
            print(f"Loaded: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")

# Merge all dataframes into a single file
if all_dataframes:
    merged_df = pd.concat(all_dataframes, ignore_index=True)
    merged_df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"✅ Concatenation complete! Saved as: {output_file}")
else:
    print("⚠️ No valid Excel files found for merging.")
