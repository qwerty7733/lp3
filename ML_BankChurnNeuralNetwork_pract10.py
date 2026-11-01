# ML Practical 10: Neural network to predict if a bank customer will leave (Exited = 1) in 6 months
# Steps: read data -> features & target -> split -> normalize -> build model -> evaluate -> improve

import os                                     # os builds file paths
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"      # hide TensorFlow's long info messages
import pandas as pd                           # pandas reads and prepares the data
from sklearn.model_selection import train_test_split          # splits data into train and test
from sklearn.preprocessing import StandardScaler              # normalizes features (mean 0, std 1)
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report   # evaluation
from tensorflow import keras                                  # Keras API to build neural networks

HERE = os.path.dirname(os.path.abspath(__file__))             # folder of this script
df = pd.read_csv(os.path.join(HERE, "..", "datasets", "Churn_Modelling.csv"))   # 10,000 customers
print("Shape:", df.shape)                                     # (rows, columns)

# ---------------- 1. Feature set and target ----------------
df = df.drop(columns=["RowNumber", "CustomerId", "Surname"])  # IDs and names do not affect leaving
df["Gender"] = df["Gender"].map({"Female": 0, "Male": 1})     # convert text to numbers
df = pd.get_dummies(df, columns=["Geography"], dtype=int)     # one-hot: France/Germany/Spain -> 3 columns of 0/1
X = df.drop(columns=["Exited"])                               # features (inputs)
y = df["Exited"]                                              # target: 1 = left, 0 = stayed

# ---------------- 2. Train / test split ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1, stratify=y)          # 8000 train, 2000 test

# ---------------- 3. Normalize ----------------
scaler = StandardScaler()                                     # (x - mean) / std for every column
X_train = scaler.fit_transform(X_train)                       # learn mean/std on training data and apply
X_test = scaler.transform(X_test)                             # apply the SAME mean/std to test data


def evaluate(name, model):                                    # print the results of one model
    pred = (model.predict(X_test, verbose=0) > 0.5).astype(int).ravel()   # probability > 0.5 -> class 1
    print("\n" + "=" * 50)                                    # separator
    print(name)                                               # model name
    print("Accuracy:", round(accuracy_score(y_test, pred), 4))  # fraction correct
    print("Confusion matrix:\n", confusion_matrix(y_test, pred))  # [[TN FP] [FN TP]]
    print(classification_report(y_test, pred, target_names=["Stayed", "Left"]))   # precision/recall/F1


# ---------------- 4. Basic model ----------------
model = keras.Sequential([                                    # layers stacked one after another
    keras.layers.Input(shape=(X_train.shape[1],)),            # input layer: one neuron per feature
    keras.layers.Dense(6, activation="relu"),                 # hidden layer 1: 6 neurons, ReLU activation
    keras.layers.Dense(6, activation="relu"),                 # hidden layer 2: 6 neurons
    keras.layers.Dense(1, activation="sigmoid"),              # output: probability (0..1) that customer leaves
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])   # how the model learns
model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)   # train for 50 passes over the data
evaluate("Basic model (6-6-1)", model)                        # show results

# ---------------- 5. Improved model ----------------
# Only ~20% customers leave, so the basic model misses many of them (low recall for "Left").
# Improvements: more neurons, Dropout (less overfitting), EarlyStopping, class weights.
better = keras.Sequential([                                   # a bigger network
    keras.layers.Input(shape=(X_train.shape[1],)),            # input layer
    keras.layers.Dense(32, activation="relu"),                # 32 neurons
    keras.layers.Dropout(0.2),                                # randomly switch off 20% neurons while training
    keras.layers.Dense(16, activation="relu"),                # 16 neurons
    keras.layers.Dense(1, activation="sigmoid"),              # output probability
])
better.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])   # same settings
stop = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)   # stop when validation loss stops improving
better.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2,
           callbacks=[stop], class_weight={0: 1, 1: 2}, verbose=0)   # "Left" mistakes count double
evaluate("Improved model (32-16-1 + Dropout + EarlyStopping + class weights)", better)
