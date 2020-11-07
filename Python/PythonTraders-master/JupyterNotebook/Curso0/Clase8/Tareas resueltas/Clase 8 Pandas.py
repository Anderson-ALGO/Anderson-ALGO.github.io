# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 22:21:39 2020

@author: Lucas
"""


#### Ejercicio 1 ##############################################################

lista = [[1,2,3], [4,5,6], [7,8,9]]
import pandas as pd
dataframe = pd.DataFrame(lista)
dataframe

#### Ejercicio 2 ##############################################################

data = [["NYSE",1300],["BME",2000],["BMV",3000],["BYMA",2340], ["BVC", 4000]]
columnas = ["Mercado", "Saldo"]
df2 = pd.DataFrame(data, columns = columnas)
df2

#### Ejercicio 3 ##############################################################

data = {'Indices':['DowJones', 'IBEX35', 'IndiceEuro', 'DAX'], 'Cotizaciones':[26428,6877.40,103.95,2313.36]}
df3 = pd.DataFrame(data)
df3

#### Ejercicio 4 ##############################################################

ypfd = pd.read_excel("YPF.xlsx")
ypfd
ypfd_mod = ypfd[["timestamp", "high", "volume"]]
ypfd_mod

#### Ejercicio 5 ##############################################################

ypfd
spy = pd.read_excel("SPY.xlsx")
spy
ypfd_spy = pd.concat([ypfd["adjusted_close"], spy["adjusted_close"]], join = "outer", axis = 1)
ypfd_spy

#### Ejercicio 6 ##############################################################

ypfd = pd.read_excel("YPF.xlsx")
ypfd = ypfd.sort_index(axis = 0, ascending = False)
ypfd
-------------------------------------------------------------------------------

ypfd['MA_21'] = ypfd['close'].rolling(21).mean()
ypfd['MA_42'] = ypfd['close'].rolling(42).mean()
ypfd['MA_200'] = ypfd['close'].rolling(200).mean()
ypfd

-------------------------------------------------------------------------------
ypfd_high_array = np.array(ypfd["high"])
ypfd_low_array = np.array(ypfd["low"])
ypfd_close_array = np.array(ypfd["close"])
ypfd_sum_array = ypfd_high_array + ypfd_low_array + ypfd_close_array
TP_array = ypfd_sum_array / 3
TP_array
ypfd["TP"] = pd.DataFrame(TP_array)
ypfd["TP"] = ypfd["TP"].values[::-1]
ypfd

ypfd["MidBand"] = ypfd["TP"].rolling(20).mean()
ypfd

ypfd["StdDev"] = 2*ypfd["TP"].rolling(20).std()
ypfd

ypfd["UpperBand"] = ypfd["MidBand"] + ypfd["StdDev"]
ypfd["LowerBand"] = ypfd["MidBand"] - ypfd["StdDev"]
ypfd
-------------------------------------------------------------------------------
ypfd["validador"] = (ypfd["MA_21"] > ypfd["MA_42"]) & (ypfd["MA_21"] > ypfd["MA_200"])
ypfd

#### Ejercicio 7 ##############################################################

import yfinance as yf
GGAL = yf.download('GGAL', start='2020-07-01', end= '2020-08-09', interval='1d')
GGAL_BA = yf.download("GGAL.BA", start="2020-07-01", end="2020-08-09", interval="1d")
ggal_full = pd.concat([GGAL, GGAL_BA], join = "outer", axis = 1)
ggal_full["CCL"] =( GGAL_BA["Close"] / (GGAL["Close"] * 10))*100
ggal_full
