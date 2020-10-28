import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

amd = pd.read_excel("AMD.xlsx")
a =  amd ["Close"]

google = pd.read_excel("GOOGL.xlsx")
b =  google ["Close"]

adobe = pd.read_excel("ADBE.xlsx")
c = adobe ["Close"]

from mpl_toolkits.mplot3d import axes3d

def grafico_3d (x, y, z,x_lable, y_label, z_label):
    fig = plt.figure()
    plt.ax1 = fig.add_subplot(111, projection = "3d")
    plt.ax1.scatter(x, y, z)
    plt.ax1.set_xlabel(x_label)
    plt.ax1.set_ylabel(y_label)
    plt.ax1.set_zlabel(z_label)
    plt.show()
        
grafico_3d(a, b, c, "AMD", "GOOGL", "ADOBE")
