#!/usr/bin/env python
# coding: utf-8

# In[8]:


import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from scipy.sparse import hstack


# In[9]:


CENTRAL_URL = "http://127.0.0.1:5000"
CSV_FILE = "crew_A.csv"  # change to crew_B.csv or crew_C.csv


# In[10]:


# -----------------------------
# Load global model
# -----------------------------
global_model = requests.get(f"{CENTRAL_URL}/global_model").json()


# In[11]:


# -----------------------------
# Load local private data
# -----------------------------
df = pd.read_csv(CSV_FILE)

y = df["Depressed"].astype(int)
df["text_combined"] = df[["text"]].fillna("").agg(" ".join, axis=1)

vectorizer = TfidfVectorizer(max_features=2000)
X_text = vectorizer.fit_transform(df["text_combined"])

num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
num_cols.remove("Depressed")

num_imputer = SimpleImputer(strategy="median")
X_num = num_imputer.fit_transform(df[num_cols])

X = hstack([X_text, X_num])

scaler = StandardScaler(with_mean=False)
X_scaled = scaler.fit_transform(X)


# In[12]:


# -----------------------------
# Train locally
# -----------------------------
model = LogisticRegression(max_iter=300)

model.fit(X_scaled, y)


# In[13]:


# -----------------------------
# Compute federated update
# -----------------------------
if global_model["coef"] is None:
    coef_delta = model.coef_
    intercept_delta = model.intercept_
else:
    coef_delta = model.coef_ - np.array(global_model["coef"])
    intercept_delta = model.intercept_ - np.array(global_model["intercept"])

update = {
    "coef_delta": coef_delta.tolist(),
    "intercept_delta": intercept_delta.tolist(),
    "n_samples": len(y)
}


# In[14]:


# -----------------------------
# Send update to central
# -----------------------------
requests.post(f"{CENTRAL_URL}/federated_update", json=update)

print("Local training complete. Update sent.")

