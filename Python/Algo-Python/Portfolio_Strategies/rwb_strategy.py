import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import warnings

yf.pdr_override()
warnings.filterwarnings('ignore')

stock = input('Enter a ticker: ')
num_of_years = input('Enter number of years: ')
num_of_years = float(num_of_years)

start = dt.date.today() - dt.timedelta(days = int(365.25*num_of_years))
now=dt.datetime.now()

while stock.lower() != 'quit':
    df=pdr.get_data_yahoo(stock,start,now).dropna()
    emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60]
    for x in emasUsed:
    	ema=x
    	df["Ema_"+str(ema)]=round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)
    
    df=df.iloc[60:]
    
    pos=0
    num=0
    percentchange=[]
    
    for i in df.index:
    	cmin=min(df["Ema_3"][i],df["Ema_5"][i],df["Ema_8"][i],df["Ema_10"][i],df["Ema_12"][i],df["Ema_15"][i],)
    	cmax=max(df["Ema_30"][i],df["Ema_35"][i],df["Ema_40"][i],df["Ema_45"][i],df["Ema_50"][i],df["Ema_60"][i],)
    
    	close=df["Adj Close"][i]
    	
    	if(cmin>cmax):
    		if(pos==0):
    			bp=close
    			pos=1
    			print("Buying now at "+str(bp))
    
    	elif(cmin<cmax):
    		if(pos==1):
    			pos=0
    			sp=close
    			print("Selling now at "+str(sp))
    			pc=(sp/bp-1)*100
    			percentchange.append(pc)
    	if(num==df["Adj Close"].count()-1 and pos==1):
    		pos=0
    		sp=close
    		print("Selling now at "+str(sp))
    		pc=(sp/bp-1)*100
    		percentchange.append(pc)
    
    	num+=1
    
    gains=0
    ng=0
    losses=0
    nl=0
    totalR=1
    
    for i in percentchange:
    	if(i>0):
    		gains+=i
    		ng+=1
    	else:
    		losses+=i
    		nl+=1
    	totalR=totalR*((i/100)+1)
    
    totalR=round((totalR-1)*100,2)
    
    if(ng>0):
    	avgGain=gains/ng
    	maxR=str(max(percentchange))
    else:
    	avgGain=0
    	maxR="undefined"
    
    if(nl>0):
    	avgLoss=losses/nl
    	maxL=str(min(percentchange))
    	ratio=str(-avgGain/avgLoss)
    else:
    	avgLoss=0
    	maxL="undefined"
    	ratio="inf"
    
    if(ng>0 or nl>0):
    	battingAvg=ng/(ng+nl)
    else:
    	battingAvg=0
    
    df['PC'] = df['Adj Close'].pct_change()
    hold = round(df['PC'].sum() * 100, 2)
    
    print()
    print(f"Results for {stock.upper()} going back to {str(start)}: ")
    print ("Number of Trades: "+str(ng+nl))
    print("Batting Avg: "+ str(battingAvg))
    print("Gain/loss ratio: "+ ratio)
    print("Average Gain: "+ str(avgGain))
    print("Average Loss: "+ str(avgLoss))
    print("Max Return: "+ maxR)
    print("Max Loss: "+ maxL)
    print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" )
    print ("Total return for a B&H strategy: " + str(hold)+'%')
    print()
            
    plt.subplots()
    plt.rcParams['figure.figsize'] = (15, 10)
    df = df.tail(252*5)
    plt.plot(df['Adj Close'], color='g')
    plt.plot(df['Ema_3'], color ='r')
    plt.plot(df['Ema_5'], color ='r')
    plt.plot(df['Ema_8'], color ='r')
    plt.plot(df['Ema_10'], color ='r')
    plt.plot(df['Ema_12'], color ='r')
    plt.plot(df['Ema_15'], color ='r')
    plt.plot(df['Ema_30'], color ='b')
    plt.plot(df['Ema_35'], color ='b')
    plt.plot(df['Ema_40'], color ='b')
    plt.plot(df['Ema_45'], color ='b')
    plt.plot(df['Ema_50'], color ='b')
    plt.plot(df['Ema_60'], color ='b')
    plt.title(f'Red White Blue Strategy for {stock.upper()} - {totalR}%')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.show()
    
    stock = input('Enter a ticker: ')