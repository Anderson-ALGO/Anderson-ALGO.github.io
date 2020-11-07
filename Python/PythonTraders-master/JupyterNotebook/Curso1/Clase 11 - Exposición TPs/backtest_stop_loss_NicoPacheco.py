
import logging
logging.basicConfig(level=logging.INFO,format='{asctime} {levelname} ({threadName:11s}) {message}', style='{')

""" /// FUNCIONES VARIAS /// """

#funcion para descargar info diaria. Para intra se utilizará alphavange
def getInfoDiaria(ticker, start="2000-01-01",interval="1d",end=None):
    """Recibe un ticjer y devuelve la info diaria historica del papel"""
    logging.info(f"importando info de {ticker} ")
    import yfinance as yf
    df=yf.download(ticker,start=start,end=end,interval=interval,auto_adjust=True)
    return df

def getDataExcel(ticker):
    '''
       SOLO SIRVE PARA EXCEL DESCARGADO DEYAHOO FINANCE
       Busca excel de datos y devuelve DF las columnas: 'Open','High','Low','Close','Volume'.
       La columna 'Close' trae el precio ajustado.
       |
       |_ ticker:  El ticker a buscar
       '''
    import pandas as pd
    try:
        data = pd.read_excel(ticker + '.xlsx').set_index('Date').sort_index()
        #data.index.names=["Date"]
        data.columns = ['Open', 'High', 'Low','Close', 'Volume']
    except:
        try:
            data = pd.read_excel('excels_csvs/ADRs/' + ticker + '.xlsx').set_index('timestamp').sort_index()
            data.columns = ['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
            data['pctChange'] = data.AdjClose.pct_change()
        except:
            data = 'Sorry man no encontre el archivo en tu directorio'
    #data = data.drop(["Borrar"],axis=1)
    return data


def cruceSMA(df,fast=10,slow=20):
    """Recibe un df y una cantidad de ruedas y devuelve una columna con el SMA_ruedas"""
    logging.info(f"Creando cruce SMA, fast: {fast} slow: {fast} ")
    df["cruce"] = round((df.Close.rolling(fast).mean() / df.Close.rolling(slow).mean() -1) *100,2)
    return df

def cruceEMA(df,fast=10,slow=20): #ewm(span=ruedas)
    """Recibe un df y una cantidad de ruedas y devuelve una columna con el SMA_ruedas"""
    logging.info(f"Creando cruce EMA, fast: {fast} slow: {fast} ")
    df["cruce"] = round((df.Close.ewm(span=fast).mean() / df.Close.ewm(span=slow).mean() - 1) * 100, 2)
    return df

def getRSI(df,ruedas=14):
    """Recibe un df y una cantidad de ruedas (por defecto 14) y devuelve una columna con el RSI"""
    logging.info(f"Creando RSI, ruedas: {ruedas}")
    import numpy as np

    df["diferencia"]=df.Close.diff()
    df["dif_pos"] = np.where(df["diferencia"] > 0,df["diferencia"],0)
    df["dif_neg"] = np.where(df["diferencia"] < 0, df["diferencia"], 0)
    df["media_pos"] = df["dif_pos"].ewm(alpha=1/ruedas).mean()
    df["media_neg"] = df["dif_neg"].ewm(alpha=1/ruedas).mean()
    df["rs"] = df["media_pos"] / abs(df["media_neg"])
    df["RSI"] = round(100 - 100 / (1 + df["rs"]),2)
    df=df.drop(["diferencia","dif_pos","dif_neg","media_pos","media_neg","rs"],axis=1)
    return df

def getMACD(df,fast=12,slow=26,signal=9):
    """Recibe un df y un numero para fast (defecto 12), slow (defecto 26) u signal (defecto 9) devuelve una columna con el MACD"""
    logging.info(f"Creando MACD")
    df["ema_fast"] = df.Close.ewm(span=fast).mean()
    df["ema_slow"] = df.Close.ewm(span=slow).mean()
    df["macd"] = df["ema_fast"] - df["ema_slow"]
    df["signal"] = df["macd"].ewm(span=signal).mean()
    df["histograma"] = df["macd"] - df["signal"]
    df = df.drop(["ema_fast", "ema_slow"], axis=1)
    return df



""" /// FUNCIONES DE BACKTEST /// """


def getAlertras(df,media=True,mediaTipo="SMA",fast=5,slow=20,buy_cr=0,sell_cr=0,
                rsi=True,rsi_q=14,buy_rsi=50,sell_rsi=35,
                stopActivado=False,porcentaje=1.0,
                tipo="both"):
    """Recibe un df y los parametros y agrega los indicadores y la señal, por ahora solo SMA, EMA, RSI y STOP LOSS
    Tambien agrega volatilidad y variacion"""
    logging.info(f"Creando Alertas")

    df["Variacion"] = data.Close.pct_change()*100
    df["Volatilidad"] = data.Variacion.rolling(250).std() * 250**0.5
    #Medias
    compraMedia=True
    ventaMedia=True
    if media:
        if mediaTipo=="SMA":
            df=cruceSMA(df,fast,slow).copy()
        else:
            df=cruceEMA(df,fast,slow).copy()
        compraMedia= df.cruce > buy_cr
        ventaMedia= df.cruce < sell_cr

    #RSI
    compraRSI=True
    ventaRSI=True
    if rsi:
        df=getRSI(df,rsi_q).copy()
        compraRSI= df.RSI > buy_rsi
        ventaRSI= df.RSI < sell_rsi

    df= getSenales(df,compraMedia,ventaMedia,compraRSI,ventaRSI,stopActivado=stopActivado,porcentaje=porcentaje,tipo=tipo)
    df.set_index("Date",inplace=True)

    return df


def getSenales(df,compraMedia,ventaMedia,compraRSI,ventaRSI,stopActivado,porcentaje,tipo):
    """ ACÁ VIENE LA LOGICA CON EL STOP LOSS
    Funcion que recibe el df y los parametros y agrega señales al df
    Primero verifico la señal de stop (verifica que esté comprado o vendido antes)
    y luego si no da STOP, pasa a la otra logica que seria si da compra o venta.
    """
    logging.info(f"Añadiendo las señales")
    copia = df.copy()
    copia = copia.reset_index()

    #ACA VIENE LA LOGICA DEL STOP LOSS
    #variable stop es un diccionario que tiene el porcentaje, el precio y el estado actual
    stop={"porcentaje":porcentaje,"pStop":False,"estado":"sin señal"}
    listaSenal=[] #esta lista la hago para luego meterlo en el df

    for i in range(len(copia)):
        precioActual = copia.loc[i]["Close"]

        if stopActivado: #verifica si se toma o no el stop loss

            if tipo != "short" and stop["estado"] == "compra" and precioActual < stop["pStop"]: #stop si es long o both y está comprado
                listaSenal.append("stop")
                stop["pStop"] = False
                stop["estado"] = "stop"
                continue
            elif tipo != "long" and stop["estado"] == "venta" and precioActual > stop["pStop"]: #stop si es short y está vendido
                listaSenal.append("stop")
                stop["pStop"] = False
                stop["estado"] = "stop"
                continue

        if compraRSI[i] and compraMedia[i]: #señal compra
            if stop["estado"] == "compra": #si ya estoy comprado no pone señal
                listaSenal.append("sin señal")

            elif tipo == "short" and stop["estado"] != "venta": #si voy short y no estoy vendido no puede comprar
                listaSenal.append("sin señal")

            else: #si estoy long/both y no estoy comprado o si estoy short y esta vendido
                listaSenal.append("compra")
                stop["pStop"] = precioActual * stop["porcentaje"] #pone el nuevo stop
                stop["estado"]="compra"

        elif ventaMedia[i] and ventaRSI[i]: #señal venta
            if stop["estado"] == "venta": #si ya estoy vendido no pone señal
                listaSenal.append("sin señal")
            elif tipo == "long" and stop["estado"] != "compra": #si voy long y no estoy comprado no puedo vender
                listaSenal.append("sin señal")
            else: #si voy short/both y no estoy vendido, o si voy long y estoy comprado
                listaSenal.append("venta")
                stop["pStop"] = precioActual * (1 + (1- stop["porcentaje"]))
                stop["estado"] = "venta"

        else: #no es ni stop, ni compra ni venta
            listaSenal.append("sin señal")

    copia["Señal"] = listaSenal


    return copia

def getActions(df,tipo="both"):
    """Recibe el df, saca los sin señal y setea si es compra o venta para los primeros y ultimos trades"""
    logging.info(f"Seteando el data frame ")
    actions = df.loc [ df.Señal != "sin señal"] . copy()
    actions = actions.reset_index()

    primera = actions.iloc[0]["Señal"]
    ultima = actions.iloc[-1]["Señal"]

    #Elimina aperturas y cierres que no tienen sentido
    if tipo == "long":
        if primera == "venta":
            actions = actions.iloc[1:]
        if ultima == "compra":
            actions = actions.iloc[:-1]

    if tipo == "short":
        if primera == "compra":
            actions = actions.iloc[1:]
        if ultima == "venta":
            actions = actions.iloc[:-1]

    actions = actions.set_index("Date")
    return actions

def getTrades(df,tipo="both"): #estoy n esto

    """toma las acciones y me arma un libro con cada trade"""
    logging.info(f"Creando libro de trades")
    trades={}
    f_ini=[]
    f_fin=[]
    p_ini=[]
    p_fin=[]
    listaSide=[]
    df=df.reset_index()
    abierto = False

    for i in range(len(df)):

        if tipo != "both": #si es diferente de both, funciona la regla de que los pares abren operacion
            # tomo los pares para empezar por el primero ya que viene seteado desde antes

            if i % 2 == 0 and i != (len(df) - 1):
                f_ini.append(df.iloc[i]["Date"])
                p_ini.append(df.iloc[i]["Close"])
                listaSide.append(tipo) #cuando abre tambien pone el side
            elif i % 2 != 0:
                f_fin.append(df.iloc[i]["Date"])
                p_fin.append(df.iloc[i]["Close"])

        else:
            senal = df.iloc[i]["Señal"] #le agrego el side
            if senal == "compra":
                direccion = "long"
            elif senal == "venta":
                direccion = "short"

            if i == 0:
                #abro el primer trade
                f_ini.append(df.iloc[i]["Date"])
                p_ini.append(df.iloc[i]["Close"])
                abierto = True
                listaSide.append(direccion)

            elif i == (len(df) - 1): #si es el ultimo, lo cierro
                f_fin.append(df.iloc[i]["Date"])
                p_fin.append(df.iloc[i]["Close"])
                break

            elif senal == "stop":
                f_fin.append(df.iloc[i]["Date"])
                p_fin.append(df.iloc[i]["Close"])
                abierto = False

            elif i>0 and senal != "stop":
                if abierto == True: #si viene un trade abierto, lo cierro y abro otro
                    f_fin.append(df.iloc[i]["Date"])
                    p_fin.append(df.iloc[i]["Close"])

                    f_ini.append(df.iloc[i]["Date"])
                    p_ini.append(df.iloc[i]["Close"])
                    listaSide.append(direccion)

                else: #si vengo de un trade cerrado, solo lo abro
                    f_ini.append(df.iloc[i]["Date"])
                    p_ini.append(df.iloc[i]["Close"])
                    abierto=True
                    listaSide.append(direccion)

    trades["Fecha_ini"]=f_ini
    trades["Precio_ini"]=p_ini
    trades["Side"] = listaSide
    trades["Fecha_fin"]=f_fin
    trades["Precio_fin"]=p_fin


    trades=pd.DataFrame(trades) #creo el data frame con el diccionario

    df = df.set_index("Date") #pongo el indice como estaba
    trades = getResult(trades)

    return trades


def getResult(df):
    """Recibe un df con acciones de compra venta y stop y le agrega el Yield y la cantidad de Dias"""
    logging.info(f"Calculando Yield y Dias")
    df["Yield"] = np.where(df["Side"] == "long",(df["Precio_fin"] / df["Precio_ini"] -1)*100,(df["Precio_ini"] / df["Precio_fin"] -1)*100)
    df["Dias"] = (df.Fecha_fin - df.Fecha_ini).dt.days

    return df

def signalMetrics(df,tipo="both"):
    """Recibe un df y un side con señales y entrega variables estadisticas. Toma tiempos comprados, vendidos
    y sin posicion que hubieran operado según la estrategia.
    -Volatilidad media
    -Variacion media
    -Cantidad total de en cada estado
    -Volumen medio de cada estado
    -Tiempo total en cada estado"""

    df_copia = df.copy()
    df_copia = seteoSignal(df_copia,tipo=tipo)

    #COMIENZO CON LAS METRICAS
    #creo las medias en base a las señales
    medias = df_copia.groupby("Señal").mean()

    #genero un df nuevo que será el de las metricas, en este caso agrego volatilidad media
    res = pd.DataFrame(medias.Volatilidad)
    res.loc["Total"] = df_copia.Volatilidad.mean()

    #variacion
    res["Variacion"] = medias.Variacion
    res.loc["Total","Variacion"] = df_copia.Variacion.mean()

    #cantidad
    res["Cantidad"] = df_copia.groupby("Señal").size()
    res.loc["Total","Cantidad"] = df_copia.Señal.count()

    #volumen
    res["Volumen"] = medias.Volume /1000000
    res.loc["Total","Volumen"] = df_copia.Volume.mean() /1000000

    #tiempo
    res["TiempoIn"] = (df_copia.groupby("Señal").size() / df_copia.Señal.count()) *100
    res.loc["Total", "TiempoIn"] = 1

    #agrupado = metricas.drop(["Close","Volume","Variacion","Volatilidad"],axis=1)
    #agrupado= agrupado.groupby("Señal").size()

    return res

def seteoSignal(df,tipo="both"): # SETEO EL DF_COPIA para poder sacar metricas
    """ Recibe el df y side de signamMetrics y lo setea para colocar el estado que hubiera estado, ya sea
    comprado, vendido o sin posicion"""

    #reviso cuando da la primer señal
    df = df.reset_index()
    for i in range(len(df)):
        senal = df.iloc[i]["Señal"]
        if senal != "sin señal":
            fechaIni = i
            break

    # reviso cuando da la ultima señal
    for x in range(len(df)-1,0,-1):
        senalFin = df.iloc[x]["Señal"]
        if senalFin != "sin señal":
            fechaFin = x
            break
    df = df.set_index("Date").sort_index()

    # interpolo para que quede el "estado"
    df = df.reset_index()
    for z in range(fechaIni,fechaFin):
        if df.loc[z,"Señal"] == "sin señal" or df.loc[z,"Señal"] == "stop":
            df.loc[z, "Señal"] = np.nan

    df["Señal"] = df.Señal.fillna(method="ffill")
    df = df.set_index("Date")

    # como tomo precios close y no podría comprar al cierre, tomo las variaciones del dia posterior
    df["Señal"] = df.Señal.shift(-1)

    # seteo si es long o short
    if tipo == "long":
        df["Señal"] = np.where(df.Señal == "venta", "sin señal",
                                     df.Señal)  # saco la posicion vendido
        df["Señal"] = np.where(df.Señal == "stop", "sin señal", df.Señal)  # saco la posicion stop
    if tipo == "short":
        df["Señal"] = np.where(df.Señal == "compra", "sin señal", df.Señal)  # saco posicion compra
        df["Señal"] = np.where(df.Señal == "stop", "sin señal", df.Señal)  # saco posicion stop

    return df


""" /// PONGO EN MARCHA LA ESTRATEGIA /// """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.max_rows=50
pd.options.display.max_columns=10

#data=getDataExcel("pruebaY")
data=getInfoDiaria("AAPL")
side = "both"

#Medias
media=True
fast=5
slow=20
mediaTipo="EMA"
buy_cr=0
sell_cr=0

#RSI
rsi=True
rsi_q=14
buy_rsi=50
sell_rsi=35

#STOPLOSS
stopActivar=True
porcen=0.9


data=data.drop(["Open","High","Low"],axis=1)
data=getAlertras(data,media=media,fast=fast, slow=slow, buy_cr=buy_cr, sell_cr=sell_cr,mediaTipo=mediaTipo,
                 rsi_q=rsi_q, buy_rsi=buy_rsi, sell_rsi=sell_rsi,rsi=rsi,
                 stopActivado=stopActivar,porcentaje=porcen,tipo=side)

print(data)

acciones=getActions(data,side)
print(acciones)

trades=getTrades(acciones,side)
print(trades)
