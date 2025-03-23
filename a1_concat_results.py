import pandas as pd
import os

input_folder = 'results'
output_folder = 'results_final'
output_file_csv = 'all_results.csv'
filtered_file_xlsx = 'filtered_cols.xlsx'

all_data = []

# Δημιουργία του καταλόγου results_final αν δεν υπάρχει
os.makedirs(output_folder, exist_ok=True)

# Διαβάζει κάθε αρχείο xlsx στον φάκελο
for filename in os.listdir(input_folder):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(input_folder, filename)
        
        # Διαβάζει το αρχείο χωρίς header για να εντοπίσει τη σωστή γραμμή
        df_raw = pd.read_excel(file_path, header=None)

        # Εντοπισμός της πρώτης γραμμής με ακριβώς 7 στήλες
        for idx, row in df_raw.iterrows():
            if row.count() == 7:
                header_index = idx
                break

        # Διαβάζει ξανά το αρχείο με σωστό header
        df_clean = pd.read_excel(file_path, header=header_index)
        df_clean['source_file'] = filename  # Προσθέτει στήλη με το όνομα του αρχείου
        all_data.append(df_clean)

# Ενοποίηση όλων των δεδομένων σε ένα DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Αποθήκευση πλήρους αρχείου σε CSV
output_path_csv = os.path.join(output_folder, output_file_csv)
final_df.to_csv(output_path_csv, index=False)

# --- Φιλτράρισμα στηλών 1,2,3,7 (δηλαδή index 0,1,2,6) ---
# filtered_df = final_df.iloc[:, [0, 1, 2, 6]]
filtered_df = final_df.iloc[:, [0, 1, 2, 6]].copy()



# Μετονομασία των στηλών (αν θέλεις καθαρά ονόματα)
filtered_df.columns = ['col1', 'col2', 'col3', 'score']

# Προσθήκη στήλης με το bonus
# filtered_df['final_score'] = filtered_df['score'] + 1.
filtered_df['final_score'] = (filtered_df['score'] + 1.33).clip(upper=20).round(2)


# Αποθήκευση σε Excel
output_path_xlsx = os.path.join(output_folder, filtered_file_xlsx)
filtered_df.to_excel(output_path_xlsx, index=False)

print(f"✅ Το πλήρες αρχείο αποθηκεύτηκε στο: {output_path_csv}")
print(f"✅ Το φιλτραρισμένο αρχείο με bonus αποθηκεύτηκε στο: {output_path_xlsx}")

# --- Δημιουργία αρχείου μόνο με col3 και final_score ---
sorted_df = filtered_df[['col3', 'final_score']].sort_values(by='col3', ascending=True)

# Αποθήκευση σε Excel
sorted_excel_path = os.path.join(output_folder, 'sorted_results.xlsx')
sorted_df.to_excel(sorted_excel_path, index=False)

# Αποθήκευση σε PDF (μέσω matplotlib)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Μετατροπή της col3 σε string (π.χ. για ΑΜ όπως "2023001")
sorted_df['col3'] = sorted_df['col3'].astype(str)

# Ορισμός κεφαλίδων ως "ΑΜ" και "Βαθμός"
pdf_headers = ['ΑΜ', 'Βαθμός']
pdf_data = sorted_df.values.tolist()

pdf_path = os.path.join(output_folder, 'sorted_results.pdf')

with PdfPages(pdf_path) as pdf:
    fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=pdf_data, colLabels=pdf_headers, cellLoc='center', loc='center')
    table.scale(1, 1.5)
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

print(f"✅ Το αρχείο με col3 και final_score αποθηκεύτηκε ως Excel: {sorted_excel_path}")
print(f"✅ Το αρχείο με col3 και final_score αποθηκεύτηκε ως PDF: {pdf_path}")

