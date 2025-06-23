import re
import numpy as np
from sklearn.ensemble import IsolationForest

LOG_PATH = "logs/laravel.log"
pattern = re.compile(r"(select\s|union\s|or\s1=1|<script>|alert\(|drop\s)", re.IGNORECASE)

def extract_features(line):
    return [
        len(line),
        int(bool(pattern.search(line))),
        line.count("="),
        line.count("'"),
        line.count("<"),
        line.count(">")
    ]

def run_detection():
    with open(LOG_PATH, "r") as f:
        lines = f.readlines()

    X = np.array([extract_features(line) for line in lines])
    clf = IsolationForest(contamination=0.05)
    clf.fit(X)
    predictions = clf.predict(X)

    flagged = []
    for i, p in enumerate(predictions):
        if p == -1:
            flagged.append(lines[i].strip())
    return flagged
