import pandas as pd

def train(csv_path):
    df = pd.read_csv(csv_path)
    return {"weight": len(df)}
