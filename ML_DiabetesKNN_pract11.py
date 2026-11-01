# ML Practical 11: K-Nearest Neighbors on diabetes.csv
# Compute: confusion matrix, accuracy, error rate, precision, recall

import os                                     # os builds file paths
import numpy as np                            # numpy for NaN and number ranges
import pandas as pd                           # pandas reads and cleans the data
from sklearn.model_selection import train_test_split, GridSearchCV   # split data, search best k
from sklearn.pipeline import make_pipeline                    # joins scaling + model into one object
from sklearn.preprocessing import StandardScaler              # puts all columns on the same scale
from sklearn.neighbors import KNeighborsClassifier            # KNN classifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score   # metrics

HERE = os.path.dirname(os.path.abspath(__file__))             # folder of this script
df = pd.read_csv(os.path.join(HERE, "..", "datasets", "diabetes.csv"))   # 768 patients
print("Shape:", df.shape)                                     # (rows, columns)

# ---------------- Pre-processing ----------------
cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]   # 0 is impossible in these columns
df[cols] = df[cols].replace(0, np.nan)                        # so treat 0 as a missing value

# outliers: count values outside the IQR (box-plot) limits in each column
q1, q3 = df.quantile(0.25), df.quantile(0.75)                 # 25th and 75th percentile of every column
iqr = q3 - q1                                                 # inter-quartile range
outliers = ((df < q1 - 1.5 * iqr) | (df > q3 + 1.5 * iqr)).sum()   # how many outliers per column
print("Outliers per column:\n", outliers)                     # print the count

print("\nCorrelation with Outcome:\n", df.corr()["Outcome"].sort_values(ascending=False).round(3))   # Glucose is highest

X = df.drop(columns=["Outcome"])                              # features
y = df["Outcome"]                                             # target: 1 = diabetic, 0 = not diabetic
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1, stratify=y)          # 80/20 split, same ratio of classes

medians = X_train.median()                                    # medians from TRAINING data only (no leakage)
X_train = X_train.fillna(medians)                             # fill missing values in training data
X_test = X_test.fillna(medians)                               # fill test data with the same training medians

# ---------------- Find the best k ----------------
pipe = make_pipeline(StandardScaler(), KNeighborsClassifier())   # scaling is redone inside every CV fold
grid = GridSearchCV(pipe, {"kneighborsclassifier__n_neighbors": range(1, 26)}, cv=5)   # try k = 1..25
grid.fit(X_train, y_train)                                    # 5-fold cross-validation for each k
best_k = grid.best_params_["kneighborsclassifier__n_neighbors"]   # k with the best average accuracy
print("\nBest k:", best_k)                                    # print it

# ---------------- Evaluate on the test data ----------------
pred = grid.predict(X_test)                                   # predictions using the best k
cm = confusion_matrix(y_test, pred)                           # 2 x 2 matrix
tn, fp, fn, tp = cm.ravel()                                   # unpack the 4 cells
print("Confusion matrix:\n", cm)                              # rows = actual, columns = predicted
print(f"TN={tn} FP={fp} FN={fn} TP={tp}")                     # the four counts
acc = accuracy_score(y_test, pred)                            # (TP + TN) / total
print("Accuracy   :", round(acc, 4))                          # correct predictions
print("Error rate :", round(1 - acc, 4))                      # wrong predictions = 1 - accuracy
print("Precision  :", round(precision_score(y_test, pred), 4))   # TP / (TP + FP): predicted diabetic who really are
print("Recall     :", round(recall_score(y_test, pred), 4))      # TP / (TP + FN): diabetic patients we found
