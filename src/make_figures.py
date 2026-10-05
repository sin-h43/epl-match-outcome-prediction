"""Create all figures + summary tables from results/*.csv."""
import sys
from pathlib import Path
import numpy as np, pandas as pd, joblib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sys.path.insert(0, str(Path(__file__).parent))
from data import load_feature_sets, LABELS, CLASS_NAMES

R = Path(__file__).resolve().parents[1] / "results"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
COL = {"F1": "#2b6cb0", "F2": "#dd8b2a", "F3": "#c0392b"}
FS, y = load_feature_sets()

res = pd.read_csv(R / "results_main.csv"); rob = pd.read_csv(R / "robustness_main.csv")
bal = pd.read_csv(R / "results_balanced.csv") if (R / "results_balanced.csv").exists() else None
agg = rob.groupby(["feature_set", "model"]).agg(rob_acc=("acc", "mean"), rob_std=("acc", "std"),
                                                rob_draw=("recall_draw", "mean"), rob_f1=("macro_f1", "mean")).reset_index()
res = res.merge(agg, on=["feature_set", "model"])
res.to_csv(R / "summary_main.csv", index=False)
models = list(dict.fromkeys(res.model))

# Fig 1 - class balance & baselines
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
vc = y.value_counts(normalize=True).reindex(LABELS) * 100
ax[0].bar([CLASS_NAMES[l] for l in LABELS], vc, color=["#3b6fd4", "#9a9a9a", "#c0392b"])
for i, v in enumerate(vc): ax[0].text(i, v + 1, f"{v:.1f}%", ha="center")
ax[0].set_ylabel("% of matches"); ax[0].set_title("Home-team outcome distribution"); ax[0].set_ylim(0, 55)
X = FS["F1"]
for l, c, n in zip(LABELS, ["#3b6fd4", "#9a9a9a", "#c0392b"], ["Loss", "Draw", "Win"]):
    m = y == l; ax[1].scatter(X[m].h_roster_rating, X[m].a_roster_rating, s=6, alpha=.45, c=c, label=n)
ax[1].set_xlabel("home roster rating"); ax[1].set_ylabel("away roster rating"); ax[1].legend(markerscale=2, frameon=False)
ax[1].set_title("Feature set F1: classes overlap heavily")
plt.tight_layout(); plt.savefig(R / "fig1_data.png"); plt.close()

# Fig 2 - accuracy by model x feature set (test + train)
fig, ax = plt.subplots(figsize=(9.5, 3.8)); w = 0.26; xs = np.arange(len(models))
for i, fs in enumerate(["F1", "F2", "F3"]):
    d = res[res.feature_set == fs].set_index("model").reindex(models)
    ax.bar(xs + (i - 1) * w, d.rob_acc, w, yerr=d.rob_std, color=COL[fs], label=f"{fs} test (mean±sd)", capsize=2)
    ax.scatter(xs + (i - 1) * w, d.train_acc, marker="_", s=180, color="k", zorder=3, label="train acc" if i == 0 else None)
ax.axhline(y.value_counts(normalize=True).max(), ls="--", c="grey"); ax.text(len(models) - .5, .466, "home-win baseline 46.2%", ha="right", va="bottom", color="grey", fontsize=8)
ax.set_ylim(0.38, 0.72); ax.set_xticks(xs); ax.set_xticklabels(models, rotation=20, ha="right"); ax.set_ylabel("Accuracy")
ax.legend(ncol=4, frameon=False, fontsize=8, loc="upper left"); ax.set_title("Test accuracy over random splits (bars) vs training accuracy (black ticks)")
plt.tight_layout(); plt.savefig(R / "fig2_accuracy.png"); plt.close()

# Fig 3 - draw recall vs accuracy (the overfitting-on-draws story), main + balanced
fig, ax = plt.subplots(figsize=(6.2, 4))
for fs in ["F1", "F2", "F3"]:
    d = res[res.feature_set == fs]; ax.scatter(d.recall_draw, d.test_acc, s=45, c=COL[fs], label=f"{fs}", edgecolor="k", lw=.4)
if bal is not None:
    ax.scatter(bal.recall_draw, bal.test_acc, s=45, marker="^", c="none", edgecolor="#555", label="class_weight=balanced")
ax.set_xlabel("Draw recall (fraction of draws correctly predicted)"); ax.set_ylabel("Test accuracy")
ax.set_title("Predicting more draws costs overall accuracy"); ax.legend(frameon=False, fontsize=8)
plt.tight_layout(); plt.savefig(R / "fig3_draw_tradeoff.png"); plt.close()

# Fig 4 - confusion matrices for best-CV F1/F2 model and a F3 model
cms = joblib.load(R / "confusion_main.pkl")
pick = [("F1", res[res.feature_set == "F1"].sort_values("cv_acc").model.iloc[-1]),
        ("F2", res[res.feature_set == "F2"].sort_values("cv_acc").model.iloc[-1]),
        ("F3", "NN (1 hidden)")]
fig, axs = plt.subplots(1, 3, figsize=(10, 3.2))
for a, (fs, nm) in zip(axs, pick):
    cm = cms[(fs, nm)]; cmn = cm / cm.sum(1, keepdims=True)
    sns.heatmap(cmn, annot=cm, fmt="d", cmap="Blues", cbar=False, ax=a, vmin=0, vmax=1,
                xticklabels=[CLASS_NAMES[l] for l in LABELS], yticklabels=[CLASS_NAMES[l] for l in LABELS])
    a.set_title(f"{fs}: {nm}", fontsize=9); a.set_xlabel("Predicted"); a.set_ylabel("Actual")
plt.tight_layout(); plt.savefig(R / "fig4_confusion.png"); plt.close()

# Markdown table
t = res.pivot(index="model", columns="feature_set", values="test_acc").reindex(models)
t2 = res.pivot(index="model", columns="feature_set", values="rob_acc").reindex(models)
with open(R / "results_table.md", "w") as f:
    f.write("| Model | F1 test | F2 test | F3 test | F1 mean(5 splits) | F2 mean | F3 mean |\n|---|---|---|---|---|---|---|\n")
    for m in models:
        f.write(f"| {m} | " + " | ".join("-" if pd.isna(t.loc[m, c]) else f"{t.loc[m, c]*100:.2f}%" for c in ["F1", "F2", "F3"]) + " | "
                + " | ".join("-" if pd.isna(t2.loc[m, c]) else f"{t2.loc[m, c]*100:.2f}%" for c in ["F1", "F2", "F3"]) + " |\n")
print(open(R / "results_table.md").read())
print(res.groupby("feature_set")[["train_acc", "test_acc", "rob_acc", "recall_draw", "draw_pred_share"]].mean().round(3))
