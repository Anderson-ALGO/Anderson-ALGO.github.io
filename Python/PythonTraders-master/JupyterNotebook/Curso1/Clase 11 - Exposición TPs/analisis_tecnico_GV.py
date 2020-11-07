#!/usr/bin/env python
# coding: utf-8

def adx(data, length=None, scalar=None, drift=None, offset=None, **kwargs):
    """Indicator: ADX"""
    
    import pandas as pd
    from pandas import DataFrame
    from pandas_ta.overlap import rma
    from pandas_ta.volatility import atr
    from pandas_ta.utils import get_drift, get_offset, verify_series, zero
    
    #transform de DataFrame into sub DF
    high = data['High']
    low = data['Low']
    close = data['Close']
    open = data['Open']
    volume = data['Volume']
    
    
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = length if length and length > 0 else 14
    scalar = float(scalar) if scalar else 100
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    atr_ = atr(high=high, low=low, close=close, length=length)

    up = high - high.shift(drift) # high.diff(drift)
    dn = low.shift(drift) - low # low.diff(-drift).shift(drift)

    pos = ((up > dn) & (up > 0)) * up
    neg = ((dn > up) & (dn > 0)) * dn

    pos = pos.apply(zero)
    neg = neg.apply(zero)

    k = scalar / atr_
    dmp = k * rma(close=pos, length=length)
    dmn = k * rma(close=neg, length=length)

    dx = scalar * (dmp - dmn).abs() / (dmp + dmn)
    adx = rma(close=dx, length=length)

    # Offset
    if offset != 0:
        dmp = dmp.shift(offset)
        dmn = dmn.shift(offset)
        adx = adx.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        adx.fillna(kwargs["fillna"], inplace=True)
        dmp.fillna(kwargs["fillna"], inplace=True)
        dmn.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        adx.fillna(method=kwargs["fill_method"], inplace=True)
        dmp.fillna(method=kwargs["fill_method"], inplace=True)
        dmn.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    adx.name = f"ADX_{length}"
    
    #dmp.name = f"DMP_{length}"
    dmp.name = f"posDI_{length}"
    
    #dmn.name = f"DMN_{length}"
    dmn.name = f"negDI_{length}"
    

    adx.category = dmp.category = dmn.category = 'trend'

    # Prepare DataFrame to return
    #data = {adx.name: adx, dmp.name: dmp, dmn.name: dmn}
    #data = {'Open': open, 'High': high, 'Low': low, 'Close': close, 'Volume': volume, dmp.name: dmp, dmn.name: dmn, adx.name: adx}
    data = pd.concat([data, dmp, dmn, adx], axis = 1) #le agregue esta fila para que me tome el DF inicial y le agregue el DMI y ADX
    #adxdf = DataFrame(data)
    #adxdf.name = f"ADX_{length}"
    #adxdf.category = 'trend'

    #return adxdf
    return data

adx.__doc__ = """Average Directional Movement (ADX)
Average Directional Movement is meant to quantify trend strength by measuring
the amount of movement in a single direction.
Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/average-directional-movement-adx/
    TA Lib Correlation: >99%
Calculation:
    DMI ADX TREND 2.0 by @TraderR0BERT, NETWORTHIE.COM
        //Created by @TraderR0BERT, NETWORTHIE.COM, last updated 01/26/2016
        //DMI Indicator
        //Resolution input option for higher/lower time frames
        study(title="DMI ADX TREND 2.0", shorttitle="ADX TREND 2.0")
        adxlen = input(14, title="ADX Smoothing")
        dilen = input(14, title="DI Length")
        thold = input(20, title="Threshold")
        threshold = thold
        //Script for Indicator
        dirmov(len) =>
            up = change(high)
            down = -change(low)
            truerange = rma(tr, len)
            plus = fixnan(100 * rma(up > down and up > 0 ? up : 0, len) / truerange)
            minus = fixnan(100 * rma(down > up and down > 0 ? down : 0, len) / truerange)
            [plus, minus]
        adx(dilen, adxlen) =>
            [plus, minus] = dirmov(dilen)
            sum = plus + minus
            adx = 100 * rma(abs(plus - minus) / (sum == 0 ? 1 : sum), adxlen)
            [adx, plus, minus]
        [sig, up, down] = adx(dilen, adxlen)
        osob=input(40,title="Exhaustion Level for ADX, default = 40")
        col = sig >= sig[1] ? green : sig <= sig[1] ? red : gray
        //Plot Definitions Current Timeframe
        p1 = plot(sig, color=col, linewidth = 3, title="ADX")
        p2 = plot(sig, color=col, style=circles, linewidth=3, title="ADX")
        p3 = plot(up, color=blue, linewidth = 3, title="+DI")
        p4 = plot(up, color=blue, style=circles, linewidth=3, title="+DI")
        p5 = plot(down, color=fuchsia, linewidth = 3, title="-DI")
        p6 = plot(down, color=fuchsia, style=circles, linewidth=3, title="-DI")
        h1 = plot(threshold, color=black, linewidth =3, title="Threshold")
        trender = (sig >= up or sig >= down) ? 1 : 0
        bgcolor(trender>0?black:gray, transp=85)
        //Alert Function for ADX crossing Threshold
        Up_Cross = crossover(up, threshold)
        alertcondition(Up_Cross, title="DMI+ cross", message="DMI+ Crossing Threshold")
        Down_Cross = crossover(down, threshold)
        alertcondition(Down_Cross, title="DMI- cross", message="DMI- Crossing Threshold")
Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 14
    scalar (float): How much to magnify. Default: 100
    drift (int): The difference period. Default: 1
    offset (int): How many periods to offset the result. Default: 0
Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
Returns:
    pd.DataFrame: adx, dmp, dmn columns.
"""

def addRSI(data, rsi_q = 14):
    import pandas as pd    
    import numpy as np
    data = data
    dif = data['Close'].diff()
    win = pd.DataFrame(np.where(dif > 0, dif, 0))
    loss = pd.DataFrame(np.where(dif < 0, abs(dif), 0))
    ema_win = win.ewm(alpha=1 / rsi_q).mean()
    ema_loss = loss.ewm(alpha=1 / rsi_q).mean()
    rs = ema_win / ema_loss
    rsi = 100 - (100 / (1 + rs))
    rsi.index = data.index
    data['rsi'] = rsi
    return data



def addMACD(data, slow=26, fast=12, suavizado=9):
    '''
    El MACD toma la columna "Close" para hacer los calculos. Enviar datos ajustados
    '''
    df = data.copy()
    df['ema_fast'] = df.Close.ewm(span=fast).mean()
    df['ema_slow'] = df.Close.ewm(span=slow).mean()
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