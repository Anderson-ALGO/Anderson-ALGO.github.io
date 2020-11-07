"""
Created on Thu Jun 25 2020

@author: Juanpy
"""

def getDataExcel(ticker):
    '''
    Busca excel de datos y devuelve DF las columnas: 'Open','High','Low','Close','AdjClose','Volume' y 'pctChange'
    |    
    |_ ticker:  El ticker a buscar
    '''
    import pandas as pd
    try:
        data = pd.read_excel('excels_csvs/'+ticker+'.xlsx').set_index('timestamp').sort_index()
        data.columns = ['Open','High','Low','Close','AdjClose','Volume']
        data['pctChange'] = data.AdjClose.pct_change()
    except:
        try:
            data = pd.read_excel('excels_csvs/ADRs/'+ticker+'.xlsx').set_index('timestamp').sort_index()
            data.columns = ['Open','High','Low','Close','AdjClose','Volume']
            data['pctChange'] = data.AdjClose.pct_change()
        except:
            data = 'Sorry man no encontre el archivo en tu directorio'
    return data



def ajustarOHLC(data):
    '''
    Toma un DataFrame Open, High, Low, Close, AdjClose y devuelve el OHLC Ajustado
    '''
    import pandas as pd
    data['factor'] = data.AdjClose / data.Close

    cols = [data.Open*data.factor, data.High*data.factor, data.Low*data.factor, 
            data.AdjClose, data.AdjClose, data.Volume]
    
    dataAj = pd.concat(cols,axis=1)
    
    dataAj.columns = ["Open","High","Low","Close","AdjClose","Volume"]
    return dataAj

def addGap(data):
    '''
    Agrega Gap a data ajustada
    data cols entrada:  Open, High, Low, Close, AdjClose, Volume
    
    '''        
    data['pctChange'] = data.AdjClose.pct_change()
    data['Price'] = data.AdjClose
    data['Mov'] = data.AdjClose.pct_change()*100
    data['OpenGap'] = (data.Open/data.Close.shift(1)-1)*100
    data['IntraMov'] = (data.Close/data.Open-1)*100   
    return data




def addRSI(data, ruedas, ruedas_pend=0):
    '''
    Agrega la columna RSI a nuestro dataframe, basado en su columna adjusted_close
    |    
    |_ data:  dataframe
    |
    |_ ruedas: integer, La cantidad de ruedas para el cálculo del RSI
    |
    |_ ruedas_pend : integer, opcional (Cantidad de ruedas para calcular pendiente del RSI y su divergencia)
    '''
    import numpy as np
    df = data.copy()
    df['dif'] = df.AdjClose.diff()
    df['win'] = np.where(df['dif'] > 0, df['dif'], 0)
    df['loss'] = np.where(df['dif'] < 0, abs(df['dif']), 0)
    df['ema_win'] = df.win.ewm(alpha=1/ruedas).mean()
    df['ema_loss'] = df.loss.ewm(alpha=1/ruedas).mean()
    df['rs'] = df.ema_win / df.ema_loss
    data['rsi'] = 100 - (100 / (1+df.rs))

    if ruedas_pend != 0:
        data['rsi_pend'] = (data.rsi/data.rsi.shift(ruedas_pend)-1)*100
        precio_pend = (data.AdjClose/data.AdjClose.shift(ruedas_pend)-1)*100
        data['rsi_div'] = data.rsi_pend * precio_pend
    return data


def analizarDivergencias(data):
    divergencias_alcistas = data.loc[(data.rsi_div.shift() < 0) & (data.rsi_pend.shift() > 0) & (data.rsi.shift() < 35)]
    divergencias_bajistas = data.loc[(data.rsi_div.shift() < 0) & (data.rsi_pend.shift() < 0) & (data.rsi.shift() > 65)]
    div = {}
    div['alcista_media'] = divergencias_alcistas.pctChange.mean()*100
    div['alcista_q'] = divergencias_alcistas.pctChange.count()
    div['bajista_media'] = divergencias_bajistas.pctChange.mean()*100
    div['bajista_q'] = divergencias_bajistas.pctChange.count()
    div['q'] = div['alcista_q']  + div['bajista_q'] 
    div['sesgo'] = div['alcista_media']  - div['bajista_media'] 
    return div


def addMACD(data, slow=26, fast=12, suavizado=9):
    df = data.copy()
    df['ema_fast'] = df.AdjClose.ewm(span=fast).mean()
    df['ema_slow'] = df.AdjClose.ewm(span=slow).mean()
    data['macd'] = df.ema_fast - df.ema_slow
    data['signal'] = data.macd.ewm(span=suavizado).mean()
    data['histograma'] = data.macd - data.signal
    data = data.dropna().round(2)
    return data


def addBollinger(data, ruedas=20, desvios=2):
    data['sma_20'] = data.AdjClose.rolling(20).mean()
    volatilidad = data.AdjClose.rolling(20).std()
    data['boll_inf'] = data.sma_20 - 2*volatilidad
    data['boll_sup'] = data.sma_20 + 2*volatilidad
    data.dropna(inplace=True)
    return data


def addSMA(data, n):
    data['sma_'+str(n)] = data.AdjClose.rolling(n).mean()
    return data

def addEMA(data, n):
    data['ema_'+str(n)] = data.AdjClose.ewm(span=n).mean()
    return data


def addFW(data, n):
    data['fw_'+str(n)] = (data.AdjClose.shift(-n) / data.AdjClose -1)*100
    return data