const pptxgen = require("pptxgenjs");
const path = require("path");
const R = path.join(__dirname, "..", "results");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625
pres.title = "EPL Match Outcome Prediction";
const DK = "12352B", MID = "1F6B45", LIME = "C8F169", INK = "1B1B1B", MUT = "5B6B62", BG = "F6F8F4", WHITE = "FFFFFF", RED = "C0392B", BLUE = "2B6CB0", AMB = "DD8B2A";
const HF = "Cambria", BF = "Calibri";
const shadow = () => ({ type: "outer", color: "000000", blur: 6, offset: 2, angle: 90, opacity: 0.12 });

function title(s, t, dark) {
  s.addText(t, { x: 0.5, y: 0.3, w: 9, h: 0.75, fontFace: HF, fontSize: 30, bold: true, color: dark ? WHITE : DK, margin: 0, isTextBox: true });
}
function footer(s, n, dark) {
  s.addText(`EPL Match Prediction  |  ${n}`, { x: 0.5, y: 5.2, w: 9, h: 0.25, fontFace: BF, fontSize: 9, color: dark ? "9DB8A8" : MUT, margin: 0, isTextBox: true });
}
function card(s, x, y, w, h, fill) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill || WHITE }, rectRadius: 0.08, shadow: shadow(), line: { color: "E3E8E2", width: 0.5 } });
}

// 1 Title
let s = pres.addSlide(); s.background = { color: DK };
s.addShape(pres.shapes.OVAL, { x: 7.1, y: 0.9, w: 2.6, h: 2.6, fill: { color: MID }, line: { color: LIME, width: 2 } });
s.addText("57%", { x: 7.1, y: 1.5, w: 2.6, h: 0.9, fontFace: HF, fontSize: 48, bold: true, color: LIME, align: "center", margin: 0, isTextBox: true });
s.addText("from squad\nratings alone", { x: 7.1, y: 2.35, w: 2.6, h: 0.7, fontFace: BF, fontSize: 13, color: WHITE, align: "center", margin: 0, isTextBox: true });
s.addText("Predicting English Premier League Match Outcomes", { x: 0.6, y: 1.2, w: 6.3, h: 1.6, fontFace: HF, fontSize: 34, bold: true, color: WHITE, margin: 0, isTextBox: true });
s.addText("Win, draw or loss from pre-match squad statistics", { x: 0.6, y: 2.85, w: 6.3, h: 0.4, fontFace: BF, fontSize: 16, color: LIME, margin: 0, isTextBox: true });
s.addText([{ text: "UE24CS352A Machine Learning - Mini-Project", options: { breakLine: true } },
  { text: "Sinchana K (PES1UG24AM405)", options: { breakLine: true } }, { text: "Sanjana Shastry (PES1UG24AM916)" }],
  { x: 0.6, y: 3.8, w: 6.3, h: 1.0, fontFace: BF, fontSize: 14, color: "CFE0D5", margin: 0, isTextBox: true, paraSpaceAfter: 3 });
s.addNotes("Introduce team and problem. Based on Harbola & Lee (Stanford CS229, 2019). Our headline: about 57% accuracy from squad ratings alone, versus 46.2% for always guessing a home win.");

// 2 Problem
s = pres.addSlide(); s.background = { color: BG }; title(s, "The problem and the bar to beat");
s.addText("Given only pre-match information, classify a Premier League game as home win, draw or home loss.",
  { x: 0.5, y: 1.15, w: 4.6, h: 1.0, fontFace: BF, fontSize: 16, color: INK, margin: 0, isTextBox: true });
s.addText([{ text: "Why it is hard", options: { bold: true, breakLine: true } },
  { text: "Three overlapping classes", options: { bullet: true, breakLine: true } },
  { text: "Draws are the rarest outcome (24.8%)", options: { bullet: true, breakLine: true } },
  { text: "Football has high inherent randomness", options: { bullet: true } }],
  { x: 0.5, y: 2.3, w: 4.6, h: 1.9, fontFace: BF, fontSize: 15, color: INK, margin: 0, isTextBox: true, paraSpaceAfter: 6 });
const stats = [["33.3%", "random guess", MUT], ["46.2%", "always predict home win", AMB], ["~57%", "our best models", MID]];
stats.forEach((st, i) => {
  const y = 1.15 + i * 1.3; card(s, 5.6, y, 3.9, 1.1);
  s.addText(st[0], { x: 5.8, y: y + 0.1, w: 1.7, h: 0.9, fontFace: HF, fontSize: 34, bold: true, color: st[2], margin: 0, valign: "middle", isTextBox: true });
  s.addText(st[1], { x: 7.5, y: y + 0.1, w: 1.9, h: 0.9, fontFace: BF, fontSize: 14, color: INK, margin: 0, valign: "middle", isTextBox: true });
});
footer(s, 2);
s.addNotes("The real baseline is not 33%: home teams win 46.2% of the time, so a model must beat 46.2% to add value. Draws are the hardest class because they sit between wins and losses.");

// 3 Dataset
s = pres.addSlide(); s.background = { color: BG }; title(s, "Dataset: 3,791 matches, 3 feature sets");
const fsets = [["F1", "2 features", "Home and away overall roster rating", BLUE], ["F2", "10 features", "F1 + GK / DEF / MID / ATT average ratings", AMB], ["F3", "280 features", "Every player: rating, pass %, passes, shots, key passes, blocks, interceptions", RED]];
fsets.forEach((f, i) => {
  const x = 0.5 + i * 1.75; card(s, x, 1.2, 1.6, 3.7);
  s.addShape(pres.shapes.OVAL, { x: x + 0.45, y: 1.4, w: 0.7, h: 0.7, fill: { color: f[3] }, line: { color: f[3] } });
  s.addText(f[0], { x: x + 0.45, y: 1.4, w: 0.7, h: 0.7, fontFace: HF, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText(f[1], { x: x + 0.1, y: 2.25, w: 1.4, h: 0.35, fontFace: BF, fontSize: 14, bold: true, color: INK, align: "center", margin: 0, isTextBox: true });
  s.addText(f[2], { x: x + 0.12, y: 2.7, w: 1.36, h: 2.0, fontFace: BF, fontSize: 12, color: MUT, margin: 0, isTextBox: true, valign: "top" });
});
s.addChart(pres.charts.BAR, [{ name: "% of matches", labels: ["Home win", "Draw", "Home loss"], values: [46.2, 24.8, 29.0] }], {
  x: 5.85, y: 1.2, w: 3.65, h: 3.7, barDir: "col", chartColors: [MID], showTitle: true, title: "Match outcome distribution (%)", titleFontSize: 12, titleColor: INK,
  showValue: true, dataLabelFontSize: 11, dataLabelPosition: "outEnd", showLegend: false, valAxisHidden: true, valGridLine: { style: "none" }, catAxisLabelFontSize: 11, valAxisMaxVal: 55 });
footer(s, 3);
s.addNotes("Scraped from whoscored.com by the paper's authors, seasons 2009/10 to 2018/19. No missing values. Features are season-level so the model is treated as time-independent. We use their public data; the modelling and evaluation pipeline is our own.");

// 4 Approach
s = pres.addSlide(); s.background = { color: BG }; title(s, "Approach: a leakage-free pipeline");
const steps = ["Stratified 80/20 split", "Standardise features", "5-fold CV on train only", "Score test once", "Repeat on 5 more splits"];
steps.forEach((t, i) => {
  const x = 0.5 + i * 1.82; card(s, x, 1.25, 1.65, 1.35);
  s.addText(String(i + 1), { x: x + 0.12, y: 1.32, w: 0.5, h: 0.5, fontFace: HF, fontSize: 24, bold: true, color: MID, margin: 0, isTextBox: true });
  s.addText(t, { x: x + 0.12, y: 1.82, w: 1.42, h: 0.7, fontFace: BF, fontSize: 13, bold: true, color: INK, margin: 0, isTextBox: true, valign: "top" });
});
s.addText("Models compared", { x: 0.5, y: 2.95, w: 4, h: 0.4, fontFace: HF, fontSize: 20, bold: true, color: DK, margin: 0, isTextBox: true });
s.addText([{ text: "Gaussian discriminant analysis (GDA)", options: { bullet: true, breakLine: true } },
  { text: "SVM: linear, degree-5 polynomial, RBF", options: { bullet: true, breakLine: true } },
  { text: "SoftMax regression: linear and quadratic", options: { bullet: true, breakLine: true } },
  { text: "Neural network, one hidden layer", options: { bullet: true } }],
  { x: 0.5, y: 3.4, w: 4.6, h: 1.6, fontFace: BF, fontSize: 14, color: INK, margin: 0, isTextBox: true, paraSpaceAfter: 4 });
card(s, 5.5, 2.95, 4.0, 1.95, DK);
s.addText([{ text: "Beyond the paper", options: { bold: true, color: LIME, breakLine: true } },
  { text: "Hyper-parameters never see the test set", options: { bullet: true, breakLine: true } },
  { text: "Mean and spread over random splits", options: { bullet: true, breakLine: true } },
  { text: "Class-weight balancing for draws", options: { bullet: true } }],
  { x: 5.7, y: 3.05, w: 3.7, h: 1.75, fontFace: BF, fontSize: 13, color: WHITE, margin: 0, isTextBox: true, paraSpaceAfter: 4, valign: "top" });
footer(s, 4);
s.addNotes("The paper picks the best number from a single split. Differences of about 1% are within split-to-split noise, so we tune with cross-validation on train only and report mean and spread across splits.");

// 5 Implementation
s = pres.addSlide(); s.background = { color: BG }; title(s, "Implementation");
const files = [["data.py", "Loads CSVs, builds F1-F3, splits"], ["models.py", "Pipelines and hyper-parameter grids"], ["run_experiments.py", "Tune, evaluate, robustness, balanced run"], ["make_figures.py", "Figures and results tables"], ["demo.py", "Live demo with class probabilities"]];
files.forEach((f, i) => {
  const y = 1.2 + i * 0.72; card(s, 0.5, y, 5.3, 0.6);
  s.addText(f[0], { x: 0.65, y: y, w: 2.0, h: 0.6, fontFace: "Courier New", fontSize: 12, bold: true, color: MID, margin: 0, valign: "middle", isTextBox: true });
  s.addText(f[1], { x: 2.7, y: y, w: 3.0, h: 0.6, fontFace: BF, fontSize: 12, color: INK, margin: 0, valign: "middle", isTextBox: true });
});
card(s, 6.15, 1.2, 3.35, 3.5, DK);
s.addText([{ text: "Stack", options: { bold: true, color: LIME, breakLine: true } },
  { text: "Python 3, scikit-learn", options: { bullet: true, breakLine: true } }, { text: "pandas, matplotlib, seaborn", options: { bullet: true, breakLine: true } },
  { text: "Private GitHub repo with README", options: { bullet: true, breakLine: true } },
  { text: "GDA is scikit-learn QDA", options: { bullet: true, breakLine: true } },
  { text: "F3 quadratic SoftMax skipped (39k features)", options: { bullet: true } }],
  { x: 6.35, y: 1.3, w: 3.0, h: 3.3, fontFace: BF, fontSize: 13, color: WHITE, margin: 0, isTextBox: true, paraSpaceAfter: 6, valign: "top" });
footer(s, 5);
s.addNotes("Walk through the repo layout. Everything reproduces with pip install -r requirements.txt then python src/run_experiments.py. Be ready to explain any file.");

// 6 Results
s = pres.addSlide(); s.background = { color: BG }; title(s, "Result: ~57% with simple models");
const labs = ["GDA", "SVM lin", "SVM poly5", "SVM RBF", "SoftMax lin", "SoftMax quad", "NN"];
s.addChart(pres.charts.BAR, [
  { name: "F1 (2)", labels: labs, values: [56.4, 56.3, 52.1, 55.9, 56.4, 56.4, 55.7] },
  { name: "F2 (10)", labels: labs, values: [56.6, 56.7, 52.3, 56.7, 57.0, 56.6, 54.8] },
  { name: "F3 (280)", labels: labs, values: [51.4, 55.3, 47.6, 55.7, 56.2, 0, 53.0] }],
  { x: 0.4, y: 1.1, w: 6.4, h: 3.95, barDir: "col", barGrouping: "clustered", chartColors: [BLUE, AMB, RED], showLegend: true, legendPos: "b", legendFontSize: 10,
    valAxisMinVal: 40, valAxisMaxVal: 62, valAxisLabelFontSize: 10, catAxisLabelFontSize: 9, valGridLine: { color: "DDE3DC", size: 0.5 }, catGridLine: { style: "none" },
    showTitle: true, title: "Mean test accuracy (%), 5 random splits (baseline 46.2)", titleFontSize: 11, titleColor: INK });
card(s, 7.05, 1.2, 2.45, 1.7);
s.addText("57.0%", { x: 7.15, y: 1.28, w: 2.25, h: 0.7, fontFace: HF, fontSize: 34, bold: true, color: MID, align: "center", margin: 0, isTextBox: true });
s.addText("SoftMax linear on F2, best mean over splits", { x: 7.2, y: 2.0, w: 2.15, h: 0.8, fontFace: BF, fontSize: 12, color: INK, align: "center", margin: 0, isTextBox: true });
card(s, 7.05, 3.1, 2.45, 1.9);
s.addText("Good models differ by ~1%, within split noise (sd 0.7-1.8%). SoftMax quad on F3 not run.", { x: 7.2, y: 3.2, w: 2.15, h: 1.7, fontFace: BF, fontSize: 12, color: INK, margin: 0, isTextBox: true, valign: "middle" });
footer(s, 6);
s.addNotes("About 10 points above the home-win baseline. A linear model is as good as a neural network. The poly-5 SVM is the weak point in our pipeline; the paper's 58.89% for it came from a single split and we could not reproduce it (about 52% here). The zero bar for SoftMax quad on F3 means not run.");

// 7 Overfitting
s = pres.addSlide(); s.background = { color: BG }; title(s, "More features means more overfitting");
const l3 = ["GDA", "SVM lin", "SVM poly5", "SVM RBF", "SoftMax lin", "NN"];
s.addChart(pres.charts.BAR, [
  { name: "Train accuracy", labels: l3, values: [64.2, 63.1, 67.8, 77.7, 59.5, 67.9] },
  { name: "Test accuracy", labels: l3, values: [49.1, 53.9, 48.0, 54.0, 54.0, 52.3] }],
  { x: 0.4, y: 1.1, w: 6.2, h: 3.95, barDir: "col", barGrouping: "clustered", chartColors: [MID, RED], showLegend: true, legendPos: "b", legendFontSize: 10,
    valAxisMinVal: 40, valAxisMaxVal: 82, valAxisLabelFontSize: 10, catAxisLabelFontSize: 9, valGridLine: { color: "DDE3DC", size: 0.5 }, catGridLine: { style: "none" },
    showValue: true, dataLabelFontSize: 8, dataLabelPosition: "outEnd", showTitle: true, title: "Feature set F3 (280 features): train vs test (%)", titleFontSize: 11, titleColor: INK });
card(s, 6.85, 1.2, 2.65, 3.7);
s.addText([{ text: "Averaged over models", options: { bold: true, breakLine: true } },
  { text: "F1 test 56.5%", options: { breakLine: true } }, { text: "F2 test 55.4%", options: { breakLine: true } }, { text: "F3 test 51.9%", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } }, { text: "F3 has 280 features for about 3,000 training rows. Training accuracy climbs to 78% while test accuracy falls.", options: {} }],
  { x: 7.0, y: 1.35, w: 2.35, h: 3.4, fontFace: BF, fontSize: 13, color: INK, margin: 0, isTextBox: true, valign: "top", paraSpaceAfter: 3 });
footer(s, 7);
s.addNotes("This matches the paper's finding: high-variance regime with the larger feature sets. Using the 2-feature set gives the same accuracy as anything larger.");

// 8 Draws
s = pres.addSlide(); s.background = { color: BG }; title(s, "Draws are the bottleneck");
s.addImage({ path: path.join(R, "fig3_draw_tradeoff.png"), x: 0.5, y: 1.15, w: 5.4, h: 3.5 * 5.4 / 5.4 * (4 / 6.2) * 1.0 + 1.35 });
s.addText([{ text: "Well-generalising models (F1, F2) almost never predict a draw: recall at most 7%.", options: { bullet: true, breakLine: true } },
  { text: "F3 predicts more draws (recall up to 35%) but by overfitting, so accuracy drops.", options: { bullet: true, breakLine: true } },
  { text: "Class balancing lifts draw recall to 20-36% but accuracy falls to about 50-54%.", options: { bullet: true } }],
  { x: 6.15, y: 1.2, w: 3.35, h: 3.5, fontFace: BF, fontSize: 13.5, color: INK, margin: 0, isTextBox: true, paraSpaceAfter: 8, valign: "top" });
footer(s, 8);
s.addNotes("Every point is one model and feature set. Points further right predict more draws; they sit lower, meaning overall accuracy is lost. Draws sit between wins and losses in rating space, so ratings alone cannot separate them.");

// 9 Conclusions
s = pres.addSlide(); s.background = { color: DK }; title(s, "Conclusions", true);
const cons = [["Ratings work", "56-57% vs 46.2% baseline"], ["Simple wins", "Linear models match complex ones"], ["Overfit risk", "280 features: train 78%, test 54%"], ["Draws remain hard", "Need new features or models"]];
cons.forEach((c, i) => {
  const x = 0.5 + (i % 2) * 4.55, y = 1.2 + Math.floor(i / 2) * 1.35;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 4.35, h: 1.15, fill: { color: MID }, rectRadius: 0.08, line: { color: MID } });
  s.addText(c[0], { x: x + 0.2, y: y + 0.12, w: 3.95, h: 0.4, fontFace: HF, fontSize: 18, bold: true, color: LIME, margin: 0, isTextBox: true });
  s.addText(c[1], { x: x + 0.2, y: y + 0.55, w: 3.95, h: 0.45, fontFace: BF, fontSize: 14, color: WHITE, margin: 0, isTextBox: true });
});
s.addText("Reproduction note: the paper's 58.89% (poly-5 SVM) was not reproduced under a leakage-free protocol; its qualitative conclusions were.", { x: 0.5, y: 3.95, w: 9, h: 0.5, fontFace: BF, fontSize: 12, italic: true, color: "CFE0D5", margin: 0, isTextBox: true });
s.addText("Future work: form and head-to-head features, two-stage win-vs-draw models, calibration, gradient boosting.", { x: 0.5, y: 4.5, w: 9, h: 0.4, fontFace: BF, fontSize: 12, color: "CFE0D5", margin: 0, isTextBox: true });
footer(s, 9, true);
s.addNotes("Be upfront about the reproduction gap: it strengthens the credibility of the rest of the work.");

// 10 Demo
s = pres.addSlide(); s.background = { color: BG }; title(s, "Live demo");
card(s, 0.5, 1.2, 9, 2.2, "1E1E1E");
s.addText([{ text: "$ python src/demo.py --random 8", options: { breakLine: true } },
  { text: "$ python src/demo.py --home 7.15 --away 6.70", options: { breakLine: true } },
  { text: "$ python src/demo.py --interactive" }],
  { x: 0.8, y: 1.35, w: 8.4, h: 1.9, fontFace: "Courier New", fontSize: 16, color: LIME, margin: 0, isTextBox: true, valign: "middle", paraSpaceAfter: 8 });
s.addText([{ text: "Random unseen test matches: predicted vs actual, with class probabilities", options: { bullet: true, breakLine: true } },
  { text: "Custom match from home and away roster ratings", options: { bullet: true, breakLine: true } },
  { text: "Model trained on the 80% split only, so test matches are truly unseen", options: { bullet: true } }],
  { x: 0.5, y: 3.65, w: 9, h: 1.3, fontFace: BF, fontSize: 14, color: INK, margin: 0, isTextBox: true, paraSpaceAfter: 5 });
footer(s, 10);
s.addNotes("Run the three commands live. Point out that draws are rarely the top prediction even when their probability is around 25-30%. Then take questions.");

pres.writeFile({ fileName: path.join(__dirname, "..", "docs", "slides.pptx") }).then(() => console.log("ok"));
