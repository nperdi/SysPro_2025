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
            df = pd.read_excel(file_path, engine="openpyxl", header=None)
            df.insert(0, "Filename", file)  # Insert filename as the first column
            all_dataframes.append(df)
            print(f"Loaded: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")

# Merge all dataframes into a single file
if all_dataframes:
    merged_df = pd.concat(all_dataframes, ignore_index=True)

    # Find duplicate values in the 5th column (index 4)
    duplicate_values = merged_df[4].value_counts()
    repeated_values = duplicate_values[duplicate_values > 1].index.tolist()

    # Filter rows that have a duplicate value in the 5th column
    repeated_rows = merged_df[merged_df[4].isin(repeated_values)]

    # Print duplicate rows
    if not repeated_rows.empty:
        print("🔍 Rows with duplicate values in the 5th column:")
        print(repeated_rows)
    else:
        print("✅ No duplicate values found in the 5th column.")

    # Save concatenated file
    merged_df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"✅ Concatenation complete! Saved as: {output_file}")
else:
    print("⚠️ No valid Excel files found for merging.")
