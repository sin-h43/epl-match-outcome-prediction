# EPL Match Outcome Prediction (Win / Draw / Loss) — UE24CS352A Machine Learning Mini-Project

**Team**
| Member | SRN |
|---|---|
| Sinchana K | PES1UG24AM405 |
| Sanjana Shastry | PES1UG24AM916 |

**Problem:** predict the result (home win / draw / home loss) of an English Premier League match using only
information known *before* kick-off (squad ratings), following Harbola & Lee, *"Gaining a Statistical Edge in
Soccer Prediction using Machine Learning: Role of Meta Statistics in Match Prediction"* (Stanford CS229, 2019).

## Headline results (3,791 matches, 2009/10 – 2018/19)
| Baseline / model | Accuracy |
|---|---|
| Random guess | 33.3% |
| Always predict home win | 46.2% |
| Best models (SoftMax / linear SVM on F1–F2, mean of 5 random 80/20 splits) | **≈ 56–57%** |
| Same models on F3 (280 features) | 47–56%, train acc up to 78% → overfitting |

Draws remain almost unpredictable (≤ 7% draw recall for the well-generalising models); details in `docs/writeup.pdf`.

## Repository layout
```
data/      match_vectors.csv (F1/F2 features), match_vectors_extended.csv (F3 features)
src/       data.py  models.py  run_experiments.py  make_figures.py  demo.py
results/   result CSVs, figures (fig1-4), results_table.md, run_log.txt
docs/      writeup.pdf, slides.pptx
```

## Setup
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python src/run_experiments.py   # trains/tunes all models on F1,F2,F3  (~12 min on 1 CPU core) -> results/*.csv
python src/make_figures.py      # figures + results_table.md
python src/demo.py --random 8               # live demo: 8 random unseen matches, actual vs predicted
python src/demo.py --home 7.15 --away 6.70  # custom match from overall roster ratings
python src/demo.py --interactive
```

## Feature sets
| Set | Features | Count |
|---|---|---|
| F1 | home & away overall roster rating | 2 |
| F2 | F1 + GK / DEF / MID / ATT average ratings for both teams | 10 |
| F3 | per-player rating, pass %, passes/g, shots/g, key passes/g, blocks, interceptions (20 players x 2 teams) | 280 |

## Method (summary)
* Stratified 80/20 train/test split (seed 42); all features standardised inside a scikit-learn `Pipeline`.
* Hyper-parameters tuned with **5-fold CV on the training set only**; test set scored once.
* Models: GDA (QDA), SVM (linear, degree-5 polynomial, RBF), SoftMax regression (linear, quadratic features), one-hidden-layer neural network.
* Robustness: tuned models re-evaluated on 5 further random splits (mean ± sd reported).
* Extension: `class_weight="balanced"` to study the draw-recall vs accuracy trade-off.

## Data & attribution
The dataset (`match_vectors*.csv`) was scraped from whoscored.com by the paper's authors and is taken from their public repo
<https://github.com/varunharbola/EPL_match_prediction>. Feature construction, modelling pipeline, evaluation protocol,
robustness study, class-weight extension and demo in this repository are our own implementation.

## Honest notes
* The paper reports 58.89% for a degree-5 polynomial SVM on F1 from a single split. Under our leakage-free protocol
  (CV tuning, standardised features) that model reached only ~52% and was unstable; well-behaved models cluster at
  56–57%, which supports the paper's qualitative conclusions (≈ 58% is achievable from squad ratings alone;
  more features -> overfitting; draws are hard) but not that specific number.
* SoftMax with quadratic features on F3 (~39k features) was skipped as intractable, as in the paper.
