from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether

R = Path(__file__).resolve().parents[1]
H = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=2, keepWithNext=1, textColor=colors.HexColor("#1a365d"))
B = ParagraphStyle("b", fontName="Helvetica", fontSize=8.8, leading=11.2, spaceAfter=2)
BL = ParagraphStyle("bl", parent=B, leftIndent=9, bulletIndent=0)
T = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14, leading=17, spaceAfter=1)
S = ParagraphStyle("s", fontName="Helvetica", fontSize=8.8, leading=11, textColor=colors.HexColor("#444444"), spaceAfter=3)
C = ParagraphStyle("c", parent=B, fontSize=7.8, leading=9.5, textColor=colors.HexColor("#444444"))
bl = lambda t: Paragraph(t, BL, bulletText="\u2022")

doc = SimpleDocTemplate(str(R / "docs/writeup.pdf"), pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=13*mm, bottomMargin=12*mm,
                        title="EPL Match Outcome Prediction - Mini-Project Write-up", author="Sinchana K, Sanjana Shastry")
W = A4[0] - 32*mm
st = []
st += [Paragraph("Predicting English Premier League Match Outcomes with Machine Learning", T),
       Paragraph("UE24CS352A Machine Learning - Mini-Project &nbsp;|&nbsp; Sinchana K (PES1UG24AM405), Sanjana Shastry (PES1UG24AM916) "
                 "&nbsp;|&nbsp; Problem statement no.: ____ &nbsp;|&nbsp; Repo: github.com/&lt;your-username&gt;/epl-match-prediction", S)]

st += [Paragraph("1. Problem statement", H),
       Paragraph("Given only information available <b>before</b> a match (squad ratings), classify an English Premier League game as "
                 "<b>home win, draw or home loss</b>. We study and reproduce Harbola &amp; Lee (Stanford CS229, 2019), comparing several classifiers on "
                 "feature sets of increasing size and asking how much accuracy is achievable, and why draws are hard to predict.", B)]

st += [Paragraph("2. Dataset", H),
       Paragraph("3,791 EPL matches (seasons 2009/10-2018/19), scraped from whoscored.com by the paper's authors and released in their public repository. "
                 "Labels: home win 46.2%, draw 24.8%, home loss 29.0% - so random guessing gives 33.3% and <i>always predicting a home win</i> gives 46.2% "
                 "(our real baseline). Three feature sets: <b>F1</b> - home and away overall roster rating (2 features); <b>F2</b> - F1 plus GK/DEF/MID/ATT "
                 "average ratings (10); <b>F3</b> - rating, pass %, passes, shots, key passes, blocks and interceptions for every player (280). "
                 "There are no missing values; features are season-level so the model is treated as time-independent.", B)]

st += [Paragraph("3. Approach", H),
       bl("<b>Models:</b> Gaussian discriminant analysis (GDA), SVM (linear, degree-5 polynomial, RBF), SoftMax regression (linear and quadratic features), one-hidden-layer neural network."),
       bl("<b>Protocol (leakage-free):</b> stratified 80/20 split; standardisation inside a Pipeline; hyper-parameters chosen by 5-fold CV on the training set only; "
          "test set scored once. Each tuned model is re-evaluated on 5 further random splits (mean +/- sd), because single-split differences of 1% are within noise."),
       bl("<b>Metrics:</b> accuracy vs the 46.2% baseline, per-class recall (especially draws), macro-F1, confusion matrices."),
       bl("<b>Extension:</b> class-weight balancing to see whether draw recall can be raised and at what cost.")]

st += [Paragraph("4. Implementation overview", H),
       Paragraph("Python 3 / scikit-learn. <font face='Courier'>data.py</font> loads the CSVs and builds F1-F3; <font face='Courier'>models.py</font> defines the pipelines and grids; "
                 "<font face='Courier'>run_experiments.py</font> tunes, evaluates and saves results; <font face='Courier'>make_figures.py</font> produces figures/tables; "
                 "<font face='Courier'>demo.py</font> is the live demo (random unseen matches or custom home/away ratings with class probabilities). "
                 "SoftMax with quadratic features on F3 (~39k features) was skipped as intractable.", B)]

rows = [["Model", "F1", "F2", "F3", "F3 train"],
        ["GDA", "56.4", "56.6", "51.4", "64.2"], ["SVM linear", "56.3", "56.7", "55.3", "63.1"],
        ["SVM poly-5", "52.1", "52.3", "47.6", "67.8"], ["SVM RBF", "55.9", "56.7", "55.7", "77.7"],
        ["SoftMax linear", "56.4", "57.0", "56.2", "59.5"], ["SoftMax quad.", "56.4", "56.6", "-", "-"],
        ["Neural net", "55.7", "54.8", "53.0", "67.9"]]
tb = Table(rows, colWidths=[27*mm, 15*mm, 15*mm, 15*mm, 18*mm])
tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 7.8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.8),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")), ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#aaaaaa")), ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
cap = Paragraph("<b>Table 1.</b> Mean test accuracy (%) over 5 random 80/20 splits; last column = training accuracy on the main split. Baselines: random 33.3, home-win 46.2.", C)
left = [tb, Spacer(1, 2), cap]
img3 = Image(str(R / "results/fig3_draw_tradeoff.png"), width=66*mm, height=66*mm * 4/6.2)
st += [Paragraph("5. Results", H), Table([[left, [img3, Paragraph("<b>Figure 1.</b> Draw recall vs test accuracy, all runs (triangles: class-weight balanced).", C)]]], colWidths=[W - 70*mm, 70*mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)])]
st += [Image(str(R / "results/fig2_accuracy.png"), width=W * 0.86, height=W * 0.86 * 3.8 / 9.5),
       Paragraph("<b>Figure 2.</b> Test accuracy (bars, mean +/- sd over splits) vs training accuracy (black ticks).", C)]

st += [Paragraph("6. Conclusions", H),
       bl("Squad ratings alone give <b>~56-57% accuracy</b>, about 10-11 points above the home-win baseline (46.2%); the best model by CV was linear SVM on F2 (57.7% CV, 57.0% held-out), and SoftMax (linear) on F2 the best mean over splits (57.0%). "
          "Differences among the good models (~1%) are within split-to-split noise (sd 0.7-1.8%), so a <i>simple</i> model is as good as a complex one."),
       bl("<b>More features hurt:</b> on F3 training accuracy rises to 63-78% while test accuracy falls to 47-56% (overfitting; F3 has 280 features for ~3,000 training rows)."),
       bl("<b>Draws are the bottleneck:</b> on F1/F2 well-generalising models predict draws almost never (recall &lt;= 7%) because draws sit between wins and losses in rating space. "
          "F3 models predict more draws (recall up to 35%) but through overfitting, lowering accuracy. Class balancing also raises draw recall (to 20-36%) but drops accuracy to ~50-54%."),
       bl("<b>Reproduction note:</b> the paper's 58.89% (poly-5 SVM, F1) came from a single split; under our CV-tuned, standardised pipeline that model reached only ~52% and was unstable. "
          "Its qualitative findings (~57% from ratings, overfitting with larger feature sets, hard draws) are reproduced; that exact figure is not."),
       bl("<b>Future work:</b> add recent-form/head-to-head features, use ordinal or two-stage (win-vs-not, then draw) models, probability calibration, and gradient boosting."),
       Paragraph("<b>Reference:</b> V. Harbola, K. Lee, <i>Gaining a Statistical Edge in Soccer Prediction using Machine Learning</i>, CS229 Final Project, Stanford, 2019 (data and repo: github.com/varunharbola/EPL_match_prediction).", C)]
doc.build(st)
