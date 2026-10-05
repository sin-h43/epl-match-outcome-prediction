"""Live demo.

  python src/demo.py --random 8              # 8 random UNSEEN test matches: actual vs predicted
  python src/demo.py --home 7.15 --away 6.70 # custom match from overall roster ratings (F1 model)
  python src/demo.py --interactive           # keep entering ratings

Uses a multinomial-logistic (SoftMax) model with probability outputs, trained on the
80% training split only, so --random matches are genuinely unseen.
"""
import argparse, sys
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).parent))
from data import load_feature_sets, split, CLASS_NAMES

FS, y = load_feature_sets()


def fit(fs, C):
    Xtr, Xte, ytr, yte = split(FS[fs], y, seed=42)
    m = make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=3000)).fit(Xtr, ytr)
    return m, Xte, yte


def show(p, classes):
    return "  ".join(f"{CLASS_NAMES[c]} {100*pi:4.1f}%" for c, pi in zip(classes, p))


def predict_custom(h, a, model):
    x = pd.DataFrame([[h, a]], columns=["h_roster_rating", "a_roster_rating"])
    p = model.predict_proba(x)[0]; c = model.classes_
    print(f"Home {h:.2f} vs Away {a:.2f} ->  {show(p, c)}   => predicted: {CLASS_NAMES[c[p.argmax()]]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--random", type=int, default=0); ap.add_argument("--home", type=float)
    ap.add_argument("--away", type=float); ap.add_argument("--interactive", action="store_true")
    a = ap.parse_args()
    if not (a.random or a.home or a.interactive): a.random = 8
    if a.random:
        m, Xte, yte = fit("F2", 0.01)
        idx = np.random.default_rng().choice(len(Xte), a.random, replace=False)
        pr = m.predict_proba(Xte.iloc[idx]); ok = 0
        print("Model: SoftMax on F2 (10 rating features), trained on 80% split. Unseen test matches:\n")
        for i, p in zip(idx, pr):
            pred = m.classes_[p.argmax()]; act = yte.iloc[i]; ok += pred == act
            x = Xte.iloc[i]
            print(f"home {x.h_roster_rating:.2f} v away {x.a_roster_rating:.2f} | {show(p, m.classes_)} | "
                  f"pred {CLASS_NAMES[pred]:4s} actual {CLASS_NAMES[act]:4s} {'OK' if pred == act else 'x'}")
        print(f"\n{ok}/{a.random} correct in this sample. Full test accuracy: {100*m.score(Xte, yte):.2f}% "
              f"(home-win baseline 46.2%)")
    m1, _, _ = fit("F1", 0.01)
    if a.home and a.away: predict_custom(a.home, a.away, m1)
    if a.interactive:
        print("\nEnter overall roster ratings (about 6.4 - 7.5). Ctrl-C to quit.")
        while True:
            try: predict_custom(float(input("home rating: ")), float(input("away rating: ")), m1)
            except (EOFError, KeyboardInterrupt): break
            except ValueError: print("please enter numbers")


if __name__ == "__main__":
    main()
