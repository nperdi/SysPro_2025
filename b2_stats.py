import pandas as pd

# Φόρτωση του Excel
df = pd.read_excel("all_normalized_results.xlsx")

# Μετατροπή Score σε αριθμό
df["Score"] = pd.to_numeric(df["Score"], errors="coerce")

# Ομαδοποίηση ανά QuestionID και υπολογισμός
stats = df.groupby("QuestionID").agg(
    TotalAppearances=("QuestionID", "count"),
    Score_1_Count=("Score", lambda x: (x == 1).sum()),
    Score_Missing_Count=("Score", lambda x: x.isna().sum())
).reset_index()

# Αποθήκευση
stats.to_excel("question_basic_stats.xlsx", index=False)
print("📊 Σώθηκε στο 'question_basic_stats.xlsx'")
