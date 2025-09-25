# ===============================
# Chapter 1: Imports and Setup
# ===============================
# This chapter sets up the environment and dependencies for ML anomaly detection.
import os, joblib
from typing import List
import numpy as np
from pathlib import Path
from models.events import SecurityEvent, TrainResult

from sklearn.ensemble import IsolationForest

DATA_DIR = Path(os.getenv("DATA_DIR", "data")).resolve()
MODEL_DIR = DATA_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "isoforest.pkl"

FEATURES = ["https","num_links","num_forms","has_login_form"]  # simple demo features

# ===============================
# Chapter 2: Feature Engineering
# ===============================
def _featurize(events: List[SecurityEvent]) -> np.ndarray:
    """Developer Note: Converts SecurityEvent objects to feature vectors for ML."""
    X = []
    for ev in events:
        X.append([
            1 if ev.https else 0,
            ev.num_links,
            ev.num_forms,
            1 if ev.has_login_form else 0
        ])
    return np.asarray(X, dtype=float)

# ===============================
# Chapter 3: Model Training
# ===============================
def train(events: List[SecurityEvent]) -> TrainResult:
    """Developer Note: Trains an IsolationForest model on event data."""
    if not events:
        raise ValueError("No events to train on.")
    X = _featurize(events)
    clf = IsolationForest(n_estimators=100, contamination="auto", random_state=42)
    clf.fit(X)
    import joblib as _joblib
    _joblib.dump(clf, MODEL_PATH)
    return TrainResult(trained_on=len(events), model_path=str(MODEL_PATH))

# ===============================
# Chapter 4: Model Scoring
# ===============================
def score(events: List[SecurityEvent]) -> np.ndarray:
    """Developer Note: Scores events for anomaly risk using the trained model."""
    import joblib as _joblib
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found; train first.")
    clf: IsolationForest = _joblib.load(MODEL_PATH)
    X = _featurize(events)
    # Lower scores => more anomalous; convert to 0..1 risk via rank
    raw = clf.decision_function(X)  # higher is more normal
    order = raw.argsort()
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.linspace(0,1,len(raw))
    risk = 1 - ranks  # 1 = riskiest
    return risk
