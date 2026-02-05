import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load dataset
df = pd.read_csv("datasets/medical_records_train_8000.csv")

# Convert everything to strings and replace NaN with empty string
df = df.fillna("").astype(str)

# Join all columns per row safely
text_data = df.apply(lambda row: " ".join(row), axis=1)

# Build vectorizer
vec = TfidfVectorizer(max_features=2000)
vec.fit(text_data)

# Save vectorizer
joblib.dump(vec, "central_server/models/global_vectorizer.joblib")
print("TF-IDF Vectorizer built successfully!")
