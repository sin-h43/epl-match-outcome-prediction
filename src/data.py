"""Data loading and feature-set construction.

Label convention (home-team perspective): 1 = home win, 0 = draw, -1 = home loss.
F1 : home & away overall roster rating                       (2 features)
F2 : F1 + GK/DEF/MID/ATT positional average ratings          (10 features)
F3 : per-player rating + 6 per-game stats for every player  (280 features)
"""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CLASS_NAMES = {-1: "Loss", 0: "Draw", 1: "Win"}
LABELS = [-1, 0, 1]
F1_COLS = ["h_roster_rating", "a_roster_rating"]


def _read(name):
    df = pd.read_csv(DATA_DIR / name)
    df.columns = df.columns.str.strip()
    return df


def load_feature_sets():
    """Return dict {'F1','F2','F3'} -> DataFrame X, and label Series y."""
    base = _read("match_vectors.csv")
    ext = _read("match_vectors_extended.csv")
    y = base["label"].astype(int)
    assert (ext["result"].astype(int).values == y.values).all(), "row misalignment"
    X2 = base.drop(columns="label")
    return {"F1": X2[F1_COLS], "F2": X2, "F3": ext.drop(columns="result")}, y


def split(X, y, test_size=0.2, seed=42):
    return train_test_split(X, y, test_size=test_size, random_state=seed, stratify=y)
