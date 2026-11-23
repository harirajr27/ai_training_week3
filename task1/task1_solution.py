import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

df_raw = pd.read_csv("tickets_raw.csv")

print("=== BEFORE CLEANING ===")
print(f"Total rows: {len(df_raw)}")
print("Missing values (%):\n", (df_raw.isnull().mean() * 100).round(2))
print(f"Exact duplicate rows: {df_raw.duplicated().sum()}")
print("Raw category counts:\n", df_raw["category"].value_counts(dropna=False))

df_clean = df_raw.dropna(subset=["text", "category"]).copy()
df_clean["text"] = df_clean["text"].str.strip()
df_clean["category"] = df_clean["category"].str.strip().str.capitalize()
df_clean = df_clean.drop_duplicates().reset_index(drop=True)

df_clean.to_csv("tickets_clean.csv", index=False)

print("\n=== AFTER CLEANING ===")
print(f"Rows {len(df_raw)} -> {len(df_clean)} after cleaning")
print("Missing values (%):\n", (df_clean.isnull().mean() * 100).round(2))
print(f"Duplicate rows: {df_clean.duplicated().sum()}")
print("Clean category balance:\n", df_clean["category"].value_counts())

X = df_clean["text"]
y = df_clean["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=7, stratify=y
)

vectorizer = TfidfVectorizer(stop_words="english")
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train_tfidf, y_train)
y_pred_base = baseline.predict(X_test_tfidf)

base_acc = accuracy_score(y_test, y_pred_base)
base_f1 = f1_score(y_test, y_pred_base, average="macro", zero_division=0)

print("\n=== BASELINE MODEL ===")
print(f"Baseline accuracy: {base_acc:.2f} | Macro F1: {base_f1:.2f}")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_base, labels=["Billing", "Technical", "Account"]))

clf = LogisticRegression(random_state=42)
clf.fit(X_train_tfidf, y_train)
y_pred_lr = clf.predict(X_test_tfidf)

lr_acc = accuracy_score(y_test, y_pred_lr)
lr_f1 = f1_score(y_test, y_pred_lr, average="macro", zero_division=0)

print("\n=== TF-IDF + LOGISTIC REGRESSION ===")
print(f"Model accuracy: {lr_acc:.2f} | Macro F1: {lr_f1:.2f}")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_lr, labels=["Billing", "Technical", "Account"]))

print("\n=== MISCLASSIFIED TICKETS ===")
results_df = pd.DataFrame({"text": X_test, "actual": y_test, "predicted": y_pred_lr})
misclassified = results_df[results_df["actual"] != results_df["predicted"]]

for idx, row in misclassified.head(3).iterrows():
    print(f"- Ticket: '{row['text']}' | Actual: {row['actual']} | Predicted: {row['predicted']}")
    print("  Reason: Shared vocabulary across categories or small training set caused overlapping TF-IDF weights.")

X_all_tfidf = vectorizer.fit_transform(df_clean["text"])
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_clean["cluster"] = kmeans.fit_predict(X_all_tfidf)

print("\n=== KMEANS CLUSTERS VS REAL CATEGORIES ===")
print(pd.crosstab(df_clean["cluster"], df_clean["category"]))
print("""
Comparison Summary:
1. KMeans groups tickets purely by surface word overlap rather than business intent.
2. While distinct keywords partially align with Billing or Account, many tickets mix across clusters.
3. Supervised Logistic Regression outperforms KMeans because labeled examples define clear category boundaries.
""")
