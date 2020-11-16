import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as py
import plotly.graph_objs as go
from sklearn.cluster import KMeans

df = pd.read_csv("Clients.csv")

X = df[["Age", "Annual Income (k$)", "Spending Score (1-100)"]]

print(X)

algorithm = KMeans(n_clusters=6)

algorithm.fit(X)

labels = algorithm.labels_
print(labels)

centroids = algorithm.cluster_centers_
print(centroids)

df["label"] = labels
print(df)

trace1 = go.Scatter3d(
    x=df["Age"],
    y=df["Annual Income (k$)"],
    z=df["Spending Score (1-100)"],
    mode="markers",
    marker=dict(color=df["label"], size=20, line=dict(color=df["label"], width=12), opacity=0.8)
    )

data = [trace1]
layout = go.Layout(title = "Investigación de Mercado",
                   scene=dict(
                       xaxis = dict(title = "Edad"),
                       yaxis = dict(title = "Ingresos"),
                       zaxis = dict(title = "Gasto"))
                   )
