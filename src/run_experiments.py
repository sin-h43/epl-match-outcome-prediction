"""Train / tune / evaluate all models on F1, F2, F3.

Protocol
  1. Stratified 80/20 train/test split (seed 42).
  2. Hyper-parameters tuned by 5-fold CV on the TRAIN set only (no test leakage).
  3. Tuned model is refit on the full train set and scored once on the test set.
  4. Robustness: the tuned configuration is re-evaluated on N_SEEDS other random splits.
  5. Extension: class_weight='balanced' to study the draw-prediction trade-off.
Outputs are written to results/.
"""
import sys, time, warnings, json
from pathlib import Path
import numpy as np, pandas as pd, joblib
from sklearn.base import clone
from sklearn.metrics import accuracy_score, f1_score, recall_score, confusion_matrix
from sklearn.model_selection import GridSearchCV, StratifiedKFold

sys.path.insert(0, str(Path(__file__).parent))
from data import load_feature_sets, split, LABELS
from models import get_models

warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parents[1] / "results"
N_SEEDS = 5
SKIP = {("F3", "SoftMax (quad)")}   # 39k quadratic features: intractable (same as the paper)


def metrics(y_true, y_pred):
    rec = recall_score(y_true, y_pred, labels=LABELS, average=None, zero_division=0)
    return dict(acc=accuracy_score(y_true, y_pred),
                macro_f1=f1_score(y_true, y_pred, average="macro", zero_division=0),
                recall_loss=rec[0], recall_draw=rec[1], recall_win=rec[2],
                draw_pred_share=float(np.mean(y_pred == 0)))


def run(class_weight=None, tag="main", seeds=N_SEEDS, save_models=False):
    FS, y = load_feature_sets()
    rows, robust, cms, best = [], [], {}, {}
    for fs_name, X in FS.items():
        Xtr, Xte, ytr, yte = split(X, y, seed=42)
        for name, (pipe, grid) in get_models(class_weight).items():
            if (fs_name, name) in SKIP:
                continue
            t0 = time.time()
            try:
                gs = GridSearchCV(pipe, grid, cv=StratifiedKFold(5, shuffle=True, random_state=0),
                                  scoring="accuracy", n_jobs=1)
                gs.fit(Xtr, ytr)
            except Exception as e:
                print(f"[{tag}] {fs_name} {name}: FAILED ({type(e).__name__})"); continue
            model = gs.best_estimator_
            tr_acc = accuracy_score(ytr, model.predict(Xtr))
            pred = model.predict(Xte)
            m = metrics(yte, pred)
            rows.append(dict(feature_set=fs_name, model=name, n_features=X.shape[1],
                             cv_acc=gs.best_score_, train_acc=tr_acc, test_acc=m["acc"],
                             **{k: v for k, v in m.items() if k != "acc"},
                             best_params=json.dumps({k: str(v) for k, v in gs.best_params_.items()})))
            cms[(fs_name, name)] = confusion_matrix(yte, pred, labels=LABELS)
            best[(fs_name, name)] = (model, gs.best_score_)
            # robustness over random splits with tuned hyper-parameters fixed
            for s in range(seeds):
                a, b, c, d = split(X, y, seed=100 + s)
                mm = clone(model).fit(a, c)
                r = metrics(d, mm.predict(b))
                robust.append(dict(feature_set=fs_name, model=name, seed=s, **r))
            print(f"[{tag}] {fs_name:2s} {name:17s} cv={gs.best_score_:.3f} train={tr_acc:.3f} "
                  f"test={m['acc']:.3f} drawRec={m['recall_draw']:.2f} ({time.time()-t0:.0f}s)", flush=True)
    res = pd.DataFrame(rows); rob = pd.DataFrame(robust)
    res.to_csv(OUT / f"results_{tag}.csv", index=False)
    rob.to_csv(OUT / f"robustness_{tag}.csv", index=False)
    joblib.dump(cms, OUT / f"confusion_{tag}.pkl")
    if save_models:
        # choose the deployed model by CROSS-VALIDATION score (never by test score)
        (fs, nm), (mdl, sc) = max(best.items(), key=lambda kv: kv[1][1])
        Xs = FS[fs]; mdl = clone(mdl).fit(Xs, y)   # refit on all data for the demo
        joblib.dump(dict(model=mdl, feature_set=fs, name=nm, columns=list(Xs.columns), cv_acc=sc),
                    OUT / "demo_model.joblib")
        print(f"demo model = {nm} on {fs} (cv acc {sc:.3f})")
    return res, rob


if __name__ == "__main__":
    run(None, "main", save_models=True)
    run("balanced", "balanced", seeds=3)
