import yfinance as yf
import pandas as pd
import numpy as np


def getData(symbol, start='2000-01-01', interval='1d', end=None):
    data = yf.download(symbol, start=start, end=end, interval=interval, auto_adjust=True)
    return data

def getDataM(listado, start='2000-01-01', interval='1d', end=None):
    data = yf.download(listado, start=start, end=end, interval=interval, auto_adjust=True)
    return data.swaplevel(i=1, j=0, axis=1)


def addSignal(data, fast=5, slow=20, rsi_q=14, buy_cr=0, buy_rsi=60, sell_cr= -5, sell_rsi=35):
    data['Variacion'] = data.Close.pct_change()*100
    data['Volatilidad'] = data.Variacion.rolling(250).std() * 250**0.5

    data['Cruce'] = (data.Close.rolling(fast).mean() /
                     data.Close.rolling(slow).mean() - 1) * 100

    dif = data['Close'].diff()
    win = pd.DataFrame(np.where(dif > 0, dif, 0))
    loss = pd.DataFrame(np.where(dif < 0, abs(dif), 0))
    ema_win = win.ewm(alpha=1 / rsi_q).mean()
    ema_loss = loss.ewm(alpha=1 / rsi_q).mean()
    rs = ema_win / ema_loss
    rsi = 100 - (100 / (1 + rs))
    rsi.index = data.index
    data['rsi'] = rsi

    data['Señal'] = 'Sin Señal'
    comprar = (data.Cruce > buy_cr) & (data.rsi > buy_rsi)
    data.loc[comprar, 'Señal'] = 'Compra'

    vender = (data.Cruce < sell_cr) & (data.rsi < sell_rsi) 
    data.loc[vender, 'Señal'] = 'Venta'

    return data


def getActions(data, long_short='both'):
    
    # Una sola entrada y salida por vez
    actions = data.loc[data.Señal != 'Sin Señal', ['Close','Cruce','rsi','Señal']].copy()
    actions['Señal'] = np.where(actions.Señal != actions.Señal.shift(), actions.Señal,'Sin Señal')
    actions = actions.loc[actions.Señal != 'Sin Señal'].copy()    
    
    try:
        if long_short=='long':
            if actions.iloc[0,3]=='Venta':
                actions = actions.iloc[1:]
            if actions.iloc[-1,3]=='Compra':
                actions = actions.iloc[:-1]
        if long_short=='short':
            if actions.iloc[0,3]=='Compra':
                actions = actions.iloc[1:]
            if actions.iloc[-1,3]=='Venta':
                actions = actions.iloc[:-1]
    except:
        pass
            
    return actions


def getTrades(actions, long_short='both'):
    trades = []
    cerrado = True
    t = {}
    for index, row in actions.iterrows():          
        if cerrado == True:
            t['fecha_in'] = index
            t['price_in'] = row['Close']
            if row['Señal']=='Venta':
                t['side'] = 'short'
            else:
                t['side'] = 'long'   
            cerrado = False
        else:
            t['price_out'] = row['Close']
            t['fecha_out'] = index
            trades.append(t)
            cerrado = True
            t = {}
            t['fecha_in'] = index
            t['price_in'] = row['Close']
            if row['Señal']=='Venta':
                t['side'] = 'short'
            else:
                t['side'] = 'long'   
            cerrado = False
    res = pd.DataFrame(trades)
    res['yield'] = np.where(res.side=='long', res.price_out/res.price_in-1, res.price_in/res.price_out-1 )
    
    res['dias'] = (res.fecha_out - res.fecha_in).dt.days
    
    if long_short=='long':
        res = res.loc[res.side=='long']
        
    if long_short=='short':
        res = res.loc[res.side=='short']
            
    return res
    

def getSignalMetrics(df):
    df_copia = df.copy()

    # El shift(-1) es para usar las variaciones luego de las señales, ojo ahi
    df_copia['Señal'] = df_copia['Señal'].shift(-1) 
    
    #En caso de querer tomar como señales valores sin señal iterpolando, descomentar sig
    #df_copia['Señal'] = np.where(df_copia.Señal=='Sin Señal',np.nan, df_copia.Señal)
    #df_copia['Señal']  = df_copia['Señal'].fillna(method='backfill')
    
    medias = df_copia.groupby('Señal').mean()
    
    res = pd.DataFrame(medias.Volatilidad)
    res.loc['Total'] = df_copia.Volatilidad.mean()
    
    res.loc[:,'Variacion'] = medias.Variacion
    res.loc['Total', 'Variacion'] = df_copia.Variacion.mean()

    res.loc[:,'Cantidad'] = df_copia.groupby('Señal').size()
    res.loc['Total', 'Cantidad'] = len(df_copia)

    res.loc[:,'Volumen'] = medias.Volume
    res.loc['Total', 'Volumen'] = df_copia.Volume.mean()

    res.loc[:,'TiempoIn'] = round(res.Cantidad / res.Cantidad.Total,4)*100

    return res


def getTradesMetrics(trades):
    trades['factor'] =  trades['yield']+1
    longs = trades.loc[trades.side=='long']
    shorts = trades.loc[trades.side=='short']
    res = pd.DataFrame(index=['Shorts','Longs','Total'])
        
    res.loc['Longs', 'Yield %'] = (longs.factor.prod()-1)*100
    res.loc['Shorts', 'Yield %']  = (shorts.factor.prod()-1)*100
    res.loc['Total', 'Yield %']  = (trades.factor.prod()-1)*100
    
    res.loc['Longs', 'Dias']  = longs.dias.sum()
    res.loc['Shorts', 'Dias'] = shorts.dias.sum()
    res.loc['Total', 'Dias'] = trades.dias.sum()

    res['TIR %'] = np.nan
    if res.loc['Longs', 'Dias'] > 0:
        res.loc['Longs', 'TIR %'] = ((res.loc['Longs','Yield %']/100+1)**(1/(res.loc['Longs', 'Dias'] /365))-1)*100
    
    if res.loc['Shorts', 'Dias'] > 0:
        res.loc['Shorts', 'TIR %'] = ((res.loc['Shorts','Yield %']/100+1)**(1/(res.loc['Shorts', 'Dias'] /365))-1)*100
    
    if res.loc['Total', 'Dias'] > 0:    
        res.loc['Total', 'TIR %'] = ((res.loc['Total','Yield %']/100+1)**(1/(res.loc['Total', 'Dias'] /365))-1)*100

    return res.round(2)


