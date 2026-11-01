# ML Assignment 12: K-Means and Hierarchical clustering on customer data
# (Mall customers). Number of clusters is found with the elbow method.

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage

pd.set_option("display.width", 110)
pd.set_option("display.max_columns", 20)
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "outputs")
os.makedirs(OUT, exist_ok=True)

# ---------------- Read and explore the data ----------------
data = pd.read_csv(os.path.join(BASE, "datasets", "Mall_Customers.csv"))
data = data.rename(columns={"Genre": "Gender", "Annual_Income_(k$)": "Annual Income (k$)",
                            "Spending_Score": "Spending Score (1-100)"})
print("Shape:", data.shape)
print(data.head())
print("\nMissing values:", int(data.isnull().sum().sum()))
print("\nStatistics:")
print(data.describe().round(2))
print("\nCorrelation:")
print(data[["Age", "Annual Income (k$)", "Spending Score (1-100)"]].corr().round(3))

# features used for clustering: annual income and spending score
X = data[["Annual Income (k$)", "Spending Score (1-100)"]].values

# ---------------- Elbow method ----------------
wcss = []                                   # within cluster sum of squares
for k in range(1, 11):
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    km.fit(X)
    wcss.append(km.inertia_)
print("\nWCSS for k = 1 to 10:")
for k, w in enumerate(wcss, start=1):
    print(f"k = {k:<2} WCSS = {w:,.1f}")

plt.figure(figsize=(8, 4))
plt.plot(range(1, 11), wcss, marker="o", color="red", linewidth=2)
plt.xticks(range(1, 11))
plt.xlabel("Number of clusters (K)")
plt.ylabel("WCSS")
plt.title("Elbow method")
plt.grid(True)
plt.savefig(os.path.join(OUT, "ML_KMeansClustering_pract12_elbow.png"), dpi=100)
plt.close()

# choose the elbow automatically: k after which the drop in WCSS becomes small
drops = [wcss[i] - wcss[i + 1] for i in range(len(wcss) - 1)]
print("\nDrop in WCSS when going from k to k+1:", [round(d) for d in drops])
# elbow = first k for which adding one more cluster reduces WCSS by less than
# 10% of the very first drop
k_best = next(k for k in range(1, len(drops) + 1) if drops[k - 1] < 0.1 * drops[0])
print("Adding more clusters after k =", k_best, "gives only a small drop, so the elbow is at k =", k_best)

# ---------------- K-Means with the chosen number of clusters ----------------
km = KMeans(n_clusters=k_best, init="k-means++", n_init=10, random_state=42)
data["Cluster"] = km.fit_predict(X)
print(f"\nSilhouette score for k = {k_best}:", round(silhouette_score(X, data["Cluster"]), 4))
print("\nCluster sizes:")
print(data["Cluster"].value_counts().sort_index().to_string())
print("\nCluster centres (income, spending score):")
print(pd.DataFrame(km.cluster_centers_.round(1), columns=["Annual Income (k$)", "Spending Score"]))
print("\nAverage values per cluster:")
print(data.groupby("Cluster")[["Age", "Annual Income (k$)", "Spending Score (1-100)"]].mean().round(1))

plt.figure(figsize=(8, 5))
colors = ["green", "orange", "brown", "dodgerblue", "red", "purple", "olive", "cyan", "pink", "gray"]   # enough for k up to 10
for c in range(k_best):
    pts = data[data["Cluster"] == c]
    plt.scatter(pts["Annual Income (k$)"], pts["Spending Score (1-100)"], s=40, c=colors[c], label=f"Cluster {c}")
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], s=200, c="black", marker="*", label="Centroids")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.title(f"K-Means clusters (k = {k_best})")
plt.legend()
plt.savefig(os.path.join(OUT, "ML_KMeansClustering_pract12_clusters.png"), dpi=100)
plt.close()

# ---------------- K-Means on 3 features (Age, Income, Score) ----------------
X3 = data[["Age", "Annual Income (k$)", "Spending Score (1-100)"]].values
wcss3 = [KMeans(n_clusters=k, n_init=10, random_state=42).fit(X3).inertia_ for k in range(1, 11)]
print("\nWCSS with 3 features (k = 1..10):", [round(w) for w in wcss3])

# ---------------- Hierarchical clustering ----------------
Z = linkage(X, method="ward")
plt.figure(figsize=(10, 4))
dendrogram(Z, no_labels=True)
plt.title("Dendrogram (Ward linkage)")
plt.xlabel("Customers")
plt.ylabel("Euclidean distance")
plt.savefig(os.path.join(OUT, "ML_KMeansClustering_pract12_dendrogram.png"), dpi=100)
plt.close()

hc = AgglomerativeClustering(n_clusters=k_best, linkage="ward")
hc_labels = hc.fit_predict(X)
print(f"\nHierarchical clustering ({k_best} clusters) sizes:", np.bincount(hc_labels).tolist())
print("Silhouette score (hierarchical):", round(silhouette_score(X, hc_labels), 4))
