import pandas as pd
import os
import re

folder = "results_analytical"
all_normalized_rows = []

for filename in os.listdir(folder):
    if filename.endswith(".xlsx"):
        filepath = os.path.join(folder, filename)
        print(f"Επεξεργασία αρχείου: {filename}")

        try:
            # Βρες τη γραμμή με τις ερωτήσεις
            header_row = None
            for i in range(20):
                temp_df = pd.read_excel(filepath, header=None, skiprows=i, nrows=1)
                values = temp_df.iloc[0].astype(str).tolist()
                if any("id:" in val for val in values) and temp_df.shape[1] > 5:
                    header_row = i
                    break

            if header_row is None:
                print(f"⚠️ Δεν βρέθηκε γραμμή επικεφαλίδων στο αρχείο: {filename}")
                continue

            df = pd.read_excel(filepath, header=header_row)

            df.rename(columns={
                df.columns[0]: "Surname",
                df.columns[1]: "Name",
                df.columns[2]: "StudentID",
                df.columns[3]: "Email",
                df.columns[4]: "UserGroup"
            }, inplace=True)

            for _, row in df.iterrows():
                base_info = {
                    "Surname": row["Surname"],
                    "Name": row["Name"],
                    "StudentID": row["StudentID"],
                    "Email": row["Email"],
                    "UserGroup": row["UserGroup"],
                    "SourceFile": filename
                }

                for i in range(5, len(df.columns) - 1, 2):
                    question_header = df.columns[i]
                    score_col = df.columns[i + 1]
                    user_answer = row[question_header]

                    # ➤ Αν η απάντηση είναι κενή, προσπέρασέ την
                    if pd.isna(user_answer) or str(user_answer).strip() == "":
                        continue

                    # ➤ Εξαγωγή ID από την επικεφαλίδα
                    match = re.search(r'id:\s*(\d+)', str(question_header))
                    if match:
                        qid = match.group(1)
                        score = row[score_col]

                        all_normalized_rows.append({
                            **base_info,
                            "QuestionID": qid,
                            "UserAnswer": user_answer,
                            "Score": score
                        })

        except Exception as e:
            print(f"❌ Σφάλμα στο αρχείο {filename}: {e}")

# Δημιουργία και αποθήκευση
final_df = pd.DataFrame(all_normalized_rows)
final_df.to_excel("all_normalized_results.xlsx", index=False)
print("✅ Αποθηκεύτηκε στο all_normalized_results.xlsx")
