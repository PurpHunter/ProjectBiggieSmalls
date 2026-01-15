import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

dfs = [
    pd.read_csv(BASE / "devices/device_A/crew_A.csv"),
    pd.read_csv(BASE / "devices/device_B/crew_B.csv"),
    pd.read_csv(BASE / "devices/device_C/crew_C.csv"),
]

text = pd.concat(dfs)["text"].fillna("")

vectorizer = TfidfVectorizer(max_features=2000)
vectorizer.fit(text)

joblib.dump(vectorizer, BASE / "federated_learning/global_vectorizer.joblib")
