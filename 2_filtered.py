import os
import pandas as pd

# Directories
inputDir = "xls"
outputDir = "filtered_xls"

# Create the output directory if it does not exist
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

# Function to check if any cell in a row contains an "@"
def row_contains_email(row):
    return row.astype(str).str.contains("@").any()

# Process each Excel file in the input directory
for file in os.listdir(inputDir):
    if file.endswith(".xlsx"):  # Only process .xlsx files
        input_file_path = os.path.join(inputDir, file)
        output_file_path = os.path.join(outputDir, file)  # Save with the same name

        try:
            df = pd.read_excel(input_file_path, engine="openpyxl")

            # Filter rows where any column contains "@"
            df_filtered = df[df.apply(row_contains_email, axis=1)]

            # Save the filtered data
            if not df_filtered.empty:
                df_filtered.to_excel(output_file_path, index=False, header=False, engine="openpyxl")
                print(f"✅ Processed: {file} → Saved in {outputDir}/")
            else:
                print(f"⚠️ No valid emails found in {file}. Skipping saving.")

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")
