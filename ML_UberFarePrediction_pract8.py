# ML Practical 8: Predict the fare of an Uber ride
# Steps: 1) Pre-process  2) Linear Regression + Random Forest  3) Compare with R2, RMSE, MAE

import os                                     # os builds file paths that work on any computer
import numpy as np                            # numpy for maths (square root, radians, sin, cos)
import pandas as pd                           # pandas for reading and cleaning the table of data
import matplotlib                             # matplotlib for plots
matplotlib.use("Agg")                         # save plots to files instead of opening a window
import matplotlib.pyplot as plt               # plotting functions
from sklearn.model_selection import train_test_split          # splits data into train and test parts
from sklearn.linear_model import LinearRegression             # straight-line regression model
from sklearn.ensemble import RandomForestRegressor            # many decision trees averaged together
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error   # evaluation scores

HERE = os.path.dirname(os.path.abspath(__file__))             # folder of this script
DATA = os.path.join(HERE, "..", "datasets", "uber.csv")       # dataset sits in ../datasets
OUT = os.path.join(HERE, "outputs")                           # plots go into improved_code/outputs
os.makedirs(OUT, exist_ok=True)                               # create the folder if it does not exist

# ---------------- 1. Pre-processing ----------------
df = pd.read_csv(DATA)                                        # load the CSV file into a DataFrame
print("Raw shape:", df.shape)                                 # (rows, columns)
df = df.drop(columns=["Unnamed: 0", "key"])                   # these are only IDs, useless for prediction
df = df.dropna()                                              # remove rows with missing values

dt = pd.to_datetime(df["pickup_datetime"])                    # convert text date to a real date-time
df["hour"] = dt.dt.hour                                       # hour of the day (rush hour costs more)
df["weekday"] = dt.dt.weekday                                 # 0 = Monday ... 6 = Sunday
df["month"] = dt.dt.month                                     # month of the year
df["year"] = dt.dt.year                                       # fares increase over the years
df = df.drop(columns=["pickup_datetime"])                     # original text column no longer needed


def haversine(lat1, lon1, lat2, lon2):                        # distance in km between two GPS points
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])   # degrees -> radians
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * np.arcsin(np.sqrt(a))                   # 6371 km = radius of the earth


df["distance_km"] = haversine(df["pickup_latitude"], df["pickup_longitude"],
                              df["dropoff_latitude"], df["dropoff_longitude"])   # most important feature

# remove impossible values (wrong data entry)
df = df[(df["fare_amount"] > 0) & (df["distance_km"] > 0)]    # fare and distance must be positive
df = df[df["passenger_count"].between(1, 6)]                  # a car carries 1 to 6 passengers


def remove_outliers(data, col):                               # IQR (box-plot) rule for outliers
    q1, q3 = data[col].quantile([0.25, 0.75])                 # 25th and 75th percentiles
    iqr = q3 - q1                                             # inter-quartile range
    return data[data[col].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]   # keep only normal values


df = remove_outliers(df, "fare_amount")                       # remove extreme fares
df = remove_outliers(df, "distance_km")                       # remove extreme distances
print("Clean shape:", df.shape)                               # rows left after cleaning

print("\nCorrelation with fare_amount:")                      # which columns affect the fare most
print(df.corr()["fare_amount"].sort_values(ascending=False).round(3))   # distance should be highest

# ---------------- 2. Train the models ----------------
X = df.drop(columns=["fare_amount"])                          # features (inputs)
y = df["fare_amount"]                                         # target (what we predict)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)   # 80/20 split

models = {                                                    # the two models we compare
    "Linear Regression": LinearRegression(),                  # fits y = b0 + b1*x1 + b2*x2 + ...
    "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=15, random_state=42, n_jobs=-1),
}

# ---------------- 3. Evaluate and compare ----------------
print(f"\n{'Model':<20}{'R2':<8}{'RMSE':<8}{'MAE'}")          # table header
predictions = {}                                              # store predictions for the plot
for name, model in models.items():                            # train and test each model
    model.fit(X_train, y_train)                               # learn from training data
    pred = model.predict(X_test)                              # predict fares for test rides
    predictions[name] = pred                                  # keep for plotting
    r2 = r2_score(y_test, pred)                               # 1.0 = perfect, 0 = no better than the mean
    rmse = np.sqrt(mean_squared_error(y_test, pred))          # typical error in dollars (punishes big errors)
    mae = mean_absolute_error(y_test, pred)                   # average absolute error in dollars
    print(f"{name:<20}{r2:<8.4f}{rmse:<8.4f}{mae:.4f}")       # one row per model

plt.figure(figsize=(10, 4))                                   # one wide figure
for k, (name, pred) in enumerate(predictions.items()):        # one subplot per model
    plt.subplot(1, 2, k + 1)                                  # position 1 or 2
    plt.scatter(y_test.iloc[:1000], pred[:1000], s=5, alpha=0.5)   # actual vs predicted for 1000 rides
    plt.plot([0, 25], [0, 25], "r--")                         # red line = perfect prediction
    plt.xlabel("Actual fare"); plt.ylabel("Predicted fare"); plt.title(name)   # labels
plt.tight_layout()                                            # avoid overlapping labels
plt.savefig(os.path.join(OUT, "uber_actual_vs_predicted.png"))   # save the plot
print("\nHigher R2 and lower RMSE = better model (usually Random Forest).")   # conclusion
