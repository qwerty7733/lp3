# ML Practical 12: K-Means and Hierarchical clustering on mall customer data
# Number of clusters is chosen with the Elbow method.

import os                                     # os builds file paths
import pandas as pd                           # pandas reads the data
import matplotlib                             # plotting library
matplotlib.use("Agg")                         # save plots to files
import matplotlib.pyplot as plt               # plotting functions
from sklearn.cluster import KMeans, AgglomerativeClustering   # the two clustering algorithms
from sklearn.metrics import silhouette_score                  # measures how well-separated the clusters are
from scipy.cluster.hierarchy import dendrogram, linkage       # draw the hierarchical tree

HERE = os.path.dirname(os.path.abspath(__file__))             # folder of this script
OUT = os.path.join(HERE, "outputs")                           # where plots are saved
os.makedirs(OUT, exist_ok=True)                               # create folder if missing
df = pd.read_csv(os.path.join(HERE, "..", "datasets", "Mall_Customers.csv"))   # 200 customers
print(df.head())                                              # first five rows
X = df[["Annual_Income_(k$)", "Spending_Score"]].values       # cluster using income and spending score

# ---------------- Elbow method ----------------
wcss = []                                                     # within-cluster sum of squares for each k
for k in range(1, 11):                                        # try k = 1 to 10
    km = KMeans(n_clusters=k, n_init=10, random_state=42)     # k-means++ start, 10 restarts
    km.fit(X)                                                 # run the algorithm
    wcss.append(km.inertia_)                                  # inertia_ = WCSS
    print(f"k = {k:<2}  WCSS = {km.inertia_:.0f}")            # print it

plt.plot(range(1, 11), wcss, marker="o")                      # elbow curve
plt.xlabel("Number of clusters k"); plt.ylabel("WCSS"); plt.title("Elbow method")   # labels
plt.savefig(os.path.join(OUT, "kmeans_elbow.png")); plt.close()   # save and close the figure

k = 5                                                         # elbow (bend) of the curve is at k = 5
print("\nChosen k from the elbow:", k)                        # print the choice

# ---------------- K-Means with the chosen k ----------------
km = KMeans(n_clusters=k, n_init=10, random_state=42)         # final model
labels = km.fit_predict(X)                                    # cluster number (0..k-1) for each customer
print("Silhouette score (K-Means):", round(silhouette_score(X, labels), 4))   # closer to 1 = better
df["Cluster"] = labels                                        # add labels to the table
print(df.groupby("Cluster")[["Age", "Annual_Income_(k$)", "Spending_Score"]].mean().round(1))   # profile of each group

plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="tab10", s=30)   # colour each customer by cluster (works for any k)
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], c="black", marker="*", s=250)   # centroids
plt.xlabel("Annual income (k$)"); plt.ylabel("Spending score"); plt.title(f"K-Means (k = {k})")
plt.savefig(os.path.join(OUT, "kmeans_clusters.png")); plt.close()   # save the plot

# ---------------- Hierarchical clustering ----------------
plt.figure(figsize=(10, 4))                                   # wide figure for the tree
dendrogram(linkage(X, method="ward"), no_labels=True)         # Ward linkage merges clusters with least variance increase
plt.title("Dendrogram"); plt.ylabel("Distance")               # labels
plt.savefig(os.path.join(OUT, "dendrogram.png")); plt.close() # save
hc = AgglomerativeClustering(n_clusters=k, linkage="ward")    # bottom-up clustering with the same k
hc_labels = hc.fit_predict(X)                                 # cluster labels
print("Silhouette score (Hierarchical):", round(silhouette_score(X, hc_labels), 4))   # compare with K-Means
