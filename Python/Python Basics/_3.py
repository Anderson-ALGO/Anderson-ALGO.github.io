import datetime                 as dt
import matplotlib       .pyplot as plt
import matplotlib       .dates  as mdates
import pandas                   as pd
import pandas_datareader.data   as web
import numpy                    as np

start = dt.datetime(2020,10,19,0,0,0)
end   = dt.datetime(2020,10,20,0,0,0)

firm =                      "FB"
df   = web.DataReader(firm, "yahoo"        , start, end)
df  .to_excel(              "facebbok.xlsx")

# Importar Archivos Masivamente

#Importar Excel
sp500 = pd.read_excel("SP500.xlsx")
#Bajarme La Informacion
sp = sp500["MMM"]
for i in sp:
    df = web.DataReader(i, "yahoo", start, end)
    #print(df) if u want to check before the importation
    df.to_excel("{}.xlsx".format(i))
    
#Remember to pip inside anaconda
