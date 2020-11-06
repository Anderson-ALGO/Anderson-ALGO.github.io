from mplfinance.original_flavor import candlestick_ohlc
from matplotlib import dates as mdates
import datetime as dt
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
yf.pdr_override()

# input
symbol = 'AAPL'
start = dt.date.today() - dt.timedelta(days=365*4)
end = dt.date.today()

# Read data
df = yf.download(symbol, start, end)

df['HL'] = (df['High'] + df['Low'])/2
df['HLC'] = (df['High'] + df['Low'] + df['Adj Close'])/3
df['HLCC'] = (df['High'] + df['Low'] + df['Adj Close'] + df['Adj Close'])/4
df['OHLC'] = (df['Open'] + df['High'] + df['Low'] + df['Adj Close'])/4

df['Long_Cycle'] = df['Adj Close'].rolling(20).mean()
df['Short_Cycle'] = df['Adj Close'].rolling(5).mean()
df['APO'] = df['Long_Cycle'] - df['Short_Cycle']

fig = plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df['Adj Close'])
ax1.set_title('Stock ' + symbol + ' Closing Price')
ax1.set_ylabel('Price')

ax2 = plt.subplot(2, 1, 2)
ax2.plot(df['APO'], label='Absolute Price Oscillator', color='green')
ax2.grid()
ax2.set_ylabel('Absolute Price Oscillator')
ax2.set_xlabel('Date')
ax2.legend(loc='best')
plt.show()


# ## Candlestick with Absolute Price Oscillator (APO)
dfc = df.copy()
dfc['VolumePositive'] = dfc['Open'] < dfc['Adj Close']
#dfc = dfc.dropna()
dfc = dfc.reset_index()
dfc['Date'] = mdates.date2num(dfc['Date'].tolist())

fig = plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 1, 1)
candlestick_ohlc(ax1, dfc.values, width=0.5,
                 colorup='g', colordown='r', alpha=1.0)
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax1.grid(True, which='both')
ax1.minorticks_on()
ax1v = ax1.twinx()
colors = dfc.VolumePositive.map({True: 'g', False: 'r'})
ax1v.bar(dfc.Date, dfc['Volume'], color=colors, alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3*df.Volume.max())
ax1.set_title('Stock ' + symbol + ' Closing Price')
ax1.set_ylabel('Price')

ax2 = plt.subplot(2, 1, 2)
ax2.plot(df['APO'], label='Absolute Price Oscillator', color='green')
ax2.grid()
ax2.set_ylabel('Absolute Price Oscillator')
ax2.set_xlabel('Date')
ax2.legend(loc='best')
plt.show()
