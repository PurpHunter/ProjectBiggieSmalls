import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

df = pd.read_csv("datasets/medical_records_train_8000.csv")
vec = TfidfVectorizer(max_features=2000)
vec.fit(df.astype(str).agg(" ".join, axis=1))

joblib.dump(vec, "central_server/models/global_vectorizer.joblib")
