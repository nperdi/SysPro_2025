import pandas as pd
from fpdf import FPDF
import os

input_dir = "xls_concatenate"
outputDir = "pdf"
pdfTitle = "Warm-Up Exam 2025"

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

input_file = os.path.join(input_dir, "concatenated.xlsx")
output_file = os.path.join(outputDir, "warm-up_2025.pdf")

# Load the Excel file
df = pd.read_excel(input_file, header=0)

# Convert column names to strings
df.columns = df.columns.map(str)

# Print column names for debugging
print("Column Names in Excel File:", df.columns.tolist())

# Ensure we are selecting the first and sixth columns correctly
if len(df.columns) < 6:
    raise ValueError("The Excel file does not have at least 6 columns.")

# Select first and sixth column by their actual names (as strings)
first_col_name = str(df.columns[0])  # First column
sixth_col_name = str(df.columns[5])  # Sixth column

df = df[[first_col_name, sixth_col_name]]

# Sort data by the sixth column (ascending order)
df = df.sort_values(by=sixth_col_name, ascending=True)

# Add a counter column as the first column
df.insert(0, "#", range(1, len(df) + 1))

# Convert DataFrame to PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Add header
pdf.cell(200, 10, pdfTitle, ln=True, align="C")
pdf.ln(10)

# Add table headers with custom names
pdf.cell(30, 10, "#", border=1)
pdf.cell(80, 10, "Lab", border=1)
pdf.cell(80, 10, "sdi", border=1)
pdf.ln()

# Add table data
for _, row in df.iterrows():
    pdf.cell(30, 10, str(row["#"]), border=1)
    pdf.cell(80, 10, str(row[first_col_name]), border=1)
    pdf.cell(80, 10, str(row[sixth_col_name]), border=1)
    pdf.ln()

# Save to a PDF file
pdf.output(output_file)

print(f"PDF saved to {output_file}")
