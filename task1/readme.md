# Task 1: Data Audit and Model Evaluation

- **Data Cleaning:** Cleaned `tickets_raw.csv` by removing missing values, standardizing category casing, and dropping duplicates (`46 -> 35` rows).
- **Modeling:** Used an 80/20 stratified split with TF-IDF + Logistic Regression, beating the majority-class baseline on both Accuracy and Macro F1.
- **Clustering:** Ran KMeans (`k=3`) without labels, confirming supervised learning works much better because KMeans groups by word overlap rather than true intent.
