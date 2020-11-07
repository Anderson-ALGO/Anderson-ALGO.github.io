ALPHA_TOKEN  = '09QXTWMZ1UBWMPO8'
import requests 
import pandas as pd

def getData(tickers, auto_adjust='false', interval='1d', start='1980-01-01', end='2050-12-31'):
    '''
    inteervals: 1m (monthly), 1w (weekly), 1d (daily), intraday: 1min, 5min, 15min, 30min, 60min
    '''
    if interval == '1d':
        clave = 'Time Series (Daily)'
        if auto_adjust == 'true':
            function='TIME_SERIES_DAILY_ADJUSTED'
        else:
            function='TIME_SERIES_DAILY'

    elif interval == '1w':
        if auto_adjust == 'true':
            clave = 'Weekly Adjusted Time Series'
            function='TIME_SERIES_WEEKLY_ADJUSTED'
        else:
            clave = 'Weekly Time Series'
            function='TIME_SERIES_WEEKLY'
        
    elif interval == '1m':
        if auto_adjust == 'true':
            clave = 'Monthly Adjusted Time Series'
            function='TIME_SERIES_MONTHLY_ADJUSTED'
        else:
            clave = 'Monthly Time Series'
            function='TIME_SERIES_MONTHLY'
            
    else:
        clave = 'Time Series ('+interval+')'
        function='TIME_SERIES_INTRADAY'


    url = 'https://www.alphavantage.co/query'
    parametros = {'function' : function, 'symbol': tickers, 'interval':interval,
                  'outputsize': 'full', 'apikey': ALPHA_TOKEN}

    r = requests.get(url, params=parametros)

    data = r.json()[clave]
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    dataDF = dataDF.astype('float')
    dataDF.index.name = 'Date'
    
    if auto_adjust == 'true':
        if interval == '1d':
            dataDF.columns = ['Open','High','Low','Close','AdjClose','Volume','Div','Split']
            ks = dataDF['Split'].cumprod()
            dataDF['Volume'] = (dataDF['Volume']*ks)
        else:
            dataDF.columns = ['Open','High','Low','Close','AdjClose','Volume','Div']
            
        
        k = dataDF['AdjClose']/dataDF['Close']
        for column in ['Open','High','Low','Close']:
            dataDF[column] *= k
        dataDF.drop('AdjClose', axis=True, inplace=True)
    else:
        dataDF.columns = ['Open','High','Low','Close','Volume']
        
    dataDF = dataDF.sort_values('Date', ascending=True).round(2)
    dataDF.index = pd.to_datetime(dataDF.index)  
    
    dataDF = dataDF.loc[(dataDF.index>start) & (dataDF.index < end)]
    
    return dataDF




def getIntra(symbol, interval, size):
    
    function='TIME_SERIES_INTRADAY'
    url = 'https://www.alphavantage.co/query'
    parametros = {'function' : function, 'symbol': symbol, 'interval': interval, 
                  'outputsize': size, 'apikey': TOKEN}

    r = requests.get(url, params=parametros)
    data = r.json()['Time Series ('+interval+')']

    dataDF = pd.DataFrame.from_dict(data, orient='index')
    
    dataDF = dataDF.astype('float')
    
    # le pongo nombre al indice
    dataDF.index.name = 'Date'
    
    dataDF.columns = ['Open','High','Low','Close','Volume']
    dataDF['pctChange'] = dataDF.Close.pct_change()*100
    
    dataDF.index = pd.to_datetime(dataDF.index)

    dataDF = dataDF.sort_values('Date', ascending=True)
    
    return dataDF

# data = getIntra(symbol='AMZN', interval='5min', size='compact')
