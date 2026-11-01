# ML Practical 9: Email spam detection with KNN and SVM
# Binary classification: 0 = Not Spam (normal state), 1 = Spam (abnormal state)

import os                                     # os builds file paths
import pandas as pd                           # pandas reads the CSV file
from sklearn.model_selection import train_test_split          # train / test split
from sklearn.preprocessing import normalize                   # scales each email (row) to length 1
from sklearn.neighbors import KNeighborsClassifier            # K-Nearest Neighbors classifier
from sklearn.svm import SVC                                   # Support Vector Machine classifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report   # evaluation

HERE = os.path.dirname(os.path.abspath(__file__))             # folder of this script
df = pd.read_csv(os.path.join(HERE, "..", "datasets", "emails.csv"))   # 5172 emails x 3002 columns
print("Shape:", df.shape)                                     # rows = emails, columns = words
print("Missing values:", df.isnull().sum().sum())             # should be 0
print("Class counts:\n", df["Prediction"].value_counts())    # how many spam and not-spam emails

X = df.drop(columns=["Email No.", "Prediction"])              # features = count of each word in the email
y = df["Prediction"]                                          # label: 1 = spam, 0 = not spam
X = normalize(X)                                              # long and short emails become comparable

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)         # 80% train, 20% test, same spam ratio in both

models = {                                                    # the two classifiers to compare
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),         # looks at the 5 most similar emails
    "SVM (RBF kernel)": SVC(kernel="rbf", C=10),              # finds the best separating boundary
}

for name, model in models.items():                            # train and test each model
    model.fit(X_train, y_train)                               # learn from training emails
    pred = model.predict(X_test)                              # predict labels of test emails
    acc = accuracy_score(y_test, pred)                        # fraction predicted correctly
    print("\n" + "=" * 50)                                    # separator line
    print(name)                                               # model name
    print("Accuracy   :", round(acc, 4))                      # accuracy
    print("Error rate :", round(1 - acc, 4))                  # error rate = 1 - accuracy
    print("Confusion matrix [[TN FP] [FN TP]]:")              # layout of the matrix
    print(confusion_matrix(y_test, pred))                     # rows = actual, columns = predicted
    print(classification_report(y_test, pred, target_names=["Not Spam", "Spam"]))   # precision, recall, F1

print("Conclusion: SVM usually beats KNN on high-dimensional text data.")   # final remark
