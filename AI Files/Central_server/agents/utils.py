import difflib

def normalize(t):
    return " ".join(t.lower().split())

def score(a, b):
    return difflib.SequenceMatcher(None, normalize(a), normalize(b)).ratio()
