import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import numpy as np

start = dt.datetime(2010, 6, 5)
end = dt.datetime(2020, 10, 5)

firm = "EURUSD=X"
amd = web.DataReader(firm, "yahoo", start, end)
a = amd["Close"]

firm1 = "GBPUSD=X"
appl = web.DataReader(firm1, "yahoo", start, end)
b = appl["Close"]

firm2 = "USDJPY=X"
a_ = web.DataReader(firm2, "yahoo", start, end)
c = a_["Close"]

print(a.describe())
print(b.describe())
print(c.describe())

from mpl_toolkits.mplot3d import axes3d


def grafico_3d(x, y, z, x_label, y_label, z_label):
    fig = plt.figure()
    plt.ax1 = fig.add_subplot(111, projection="3d")
    plt.ax1.scatter(x, y, z)
    plt.ax1.set_xlabel(x_label)
    plt.ax1.set_ylabel(y_label)
    plt.ax1.set_zlabel(z_label)
    plt.show()


grafico_3d(a, b, c, firm, firm1, firm2)
