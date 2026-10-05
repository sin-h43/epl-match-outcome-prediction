"""Model zoo: every model is a scikit-learn Pipeline (StandardScaler -> classifier)
with a small hyper-parameter grid tuned by 5-fold CV on the training set only."""
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


def _pipe(clf):
    return Pipeline([("scale", StandardScaler()), ("clf", clf)])


def _quad(clf):
    return Pipeline([("scale", StandardScaler()),
                     ("quad", PolynomialFeatures(2, include_bias=False)),
                     ("scale2", StandardScaler()), ("clf", clf)])


def get_models(class_weight=None, seed=0):
    """name -> (pipeline, param_grid)"""
    lr = lambda: LogisticRegression(max_iter=3000, class_weight=class_weight)
    return {
        "GDA": (_pipe(QuadraticDiscriminantAnalysis()),
                {"clf__reg_param": [0.0, 0.1, 0.5, 0.9]}),
        "SVM (linear)": (_pipe(SVC(kernel="linear", class_weight=class_weight)),
                         {"clf__C": [0.01, 0.1, 1]}),
        "SVM (poly5)": (_pipe(SVC(kernel="poly", degree=5, gamma="scale", max_iter=100000, class_weight=class_weight)),
                        {"clf__C": [0.1, 1]}),
        "SVM (RBF)": (_pipe(SVC(kernel="rbf", gamma="scale", class_weight=class_weight)),
                      {"clf__C": [0.1, 1, 10]}),
        "SoftMax (linear)": (_pipe(lr()), {"clf__C": [0.001, 0.01, 0.1, 1]}),
        "SoftMax (quad)": (_quad(lr()), {"clf__C": [0.001, 0.01, 0.1, 1]}),
        "NN (1 hidden)": (_pipe(MLPClassifier(max_iter=800, early_stopping=True, random_state=seed)),
                          {"clf__hidden_layer_sizes": [(4,), (8,), (16,), (32,)],
                           "clf__alpha": [1e-3, 1e-1, 1.0]}),
    }
