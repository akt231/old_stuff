
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:55:55 2022

@author: afola
notes:
now when u run the code it selects trades , trade_listfinal---- this contains selected trades
note when a stock touches 0 on track column  it indicates a reset  usually the best time to buy (one can program a condition to buy the stock at 3percent above the close position )
Now the stock will retrace back to the upper bollinger(upper bb-column) within usually 1-3 months , in addition it retraces back to the numbers in the  Fib 100&fib764 columns 
Note that currentprice--- shows the stocks current price

so what we need to do is back testing lots of these
"""

import yfinance as yf
import pandas as pd
import numpy as np
from time import time, sleep
import datetime
from tqdm import tqdm
import math
from finvizfinance.quote import finvizfinance
import telepot



from functools import reduce      
#from ta.trend import ADXIndicator-
#rom ta import add_all_ta_features
#from ta.utils import dropna






pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


token="5270803280:AAHa3EkKzEVdSd0NHaPshl6k2ZmCs7UANPo"
reciever_id=1313067608
bot=telepot.Bot(token)
Tickers1=['brqs',"pik","reli","sxtc"]
Tickers=['MMM',
'ABT',
'ABBV',
'ABMD',
'ACN',
'ATVI',
'ADBE',
'AMD',
'AAP',

'AFL',
'A',
'APD',
'AKAM',
'ALK',
'ALB',
'ARE',
'ALGN',
'ALLE',
'LNT',
'ALL',
'GOOGL',
'GOOG',
'MO',
'AMZN',
'AMCR',
'AEE',
'AAL',
'AEP',
'AXP',
'AIG',
'AMT',
'AWK',
'AMP',
'ABC',
'AME',
#'AMGN',
'APH',
'ADI',
'ANSS',
'AON',
'AOS',
'APA',
'AIV',
'AAPL',
'AMAT',
'APTV',
'ADM',
'ARNC',
'ANET',
'AJG',
'AIZ',
'ATO',
'T',
'ADSK',
'ADP',
'AZO',
'AVB',
'AVY',
'BKR',
'BAC',
'BK',
'BAX',
'BDX',
'BBY',
'BIIB',
'BLK',
'BA',
'BKNG',
'BWA',
'BXP',
'BSX',
'BMY',
'BR',
'CHRW',
'CDNS',
'CPB',
'COF',
'CPRI',
'CAH',
'KMX',
'CCL',
'CAT',
'CBOE',
'CBRE',
'CDW',
'CE',
'CNC',
'CNP',
'CF',
'SCHW',
'CHTR',
'CVX',
'CMG',
'CB',
'CHD',
'CI',
'CINF',
'CTAS',
'CSCO',
'C',
'CFG',
'CLX',
'CME',
'CMS',
'KO',
'CTSH',
'CL',
'CMCSA',
'CMA',
'CAG',
'COP',
'ED',
'STZ',
'COO',
'CPRT',
'GLW',
'CTVA',
'COST',
'COTY',
'CCI',
'CSX',
'CMI',
'CVS',
'DHI',
'DHR',
'DRI',
'DVA',
'DE',
'DAL',
'XRAY',
'DVN',
'FANG',
'DLR',
'DFS',
'DISH',
'DG',
'DLTR',
'D',
'DOV',
'DOW',
'DTE',
'DUK',
'DD',
'DXC',
'EMN',
'ETN',
'EBAY',
'ECL',
'EIX',
'EW',
'EA',
'EMR',
'ETR',
'EOG',
'EFX',
'EQIX',
'EQR',
'ESS',
'EL',
'EVRG',
'ES',
'RE',
'EXC',
'EXPE',
'EXPD',
'EXR',
'XOM',
'FFIV',

'FAST',
'FRT',
'FDX',
'FIS',
'FITB',
'FE',
'FRC',
'FISV',
'FLT',

'FLS',
'FMC',
'F',
'FTNT',
'FTV',
'FBHS',
'FOXA',
'FOX',
'BEN',
'FCX',
'GPS',
'GRMN',
'IT',
'GD',
'GE',
'GIS',
'GM',
'GPC',
'GILD',
'GL',
'GPN',
'GS',
'GWW',
'HRB',
'HAL',
'HBI',
'HOG',
'HIG',
'HAS',
'HCA',
'PEAK',
'HP',
'HSIC',
'HSY',
'HES',
'HPE',
'HLT',
'HOLX',
'HD',
'HON',
'HRL',
'HST',
'HPQ',
'HUM',
'HBAN',
'HII',
'IEX',
'IDXX',
'ITW',
'ILMN',
'IR',
'INTC',
'ICE',
'IBM',
'INCY',
'IP',
'IPG',
'IFF',
'INTU',
'ISRG',
'IVZ',
'IPGP',
'IQV',
'IRM',
'JKHY',
'J',
'JBHT',
'SJM',
'JNJ',
'JCI',
'JPM',
'JNPR',
'K',
'KEY',
'KEYS',
'KMB',
'KIM',
'KMI',
'KLAC',
'KSS',
'KHC',
'LHX',
'LH',
'LRCX',
'LW',
'LVS',
'LEG',
'LDOS',
'LEN',
'LLY',
'LNC',
'LIN',
'LYV',
'LKQ',
'LMT',
'L',
'LOW',
'LYB',
'MTB',
'M',
'MRO',
'MPC',
'MKTX',
'MAR',
'MMC',
'MLM',
'MAS',
'MA',
'MKC',

'MCD',
'MCK',
'MDT',
'MRK',
'MET',
'MTD',
'MGM',
'MCHP',
'MU',
'MSFT',
'MAA',
'MHK',
'TAP',
'MDLZ',
'MNST',
'MCO',
'MS',
'MOS',
'MSI',
'MSCI',

'NDAQ',
'NOV',
'NTAP',
'NFLX',
'NWL',
'NEM',
'NWSA',
'NWS',
'NEE',

'NKE',
'NI',

'JWN',
'NSC',
'NTRS',
'NOC',

'NCLH',
'NRG',
'NUE',
'NVDA',
'NVR',
'ORLY',
'OXY',
'ODFL',
'OMC',
'OKE',
'ORCL',
'PCAR',
'PKG',
'PH',
'PAYX',
'PYPL',
'PNR',

'PEP',
'PKI',
'PRGO',
'PFE',
'PM',
'PSX',
'PNW',
'PXD',
'PNC',
'PPG',
'PPL',
'PFG',
'PG',
'PGR',
'PLD',
'PRU',
'PEG',
'PSA',
'PHM',
'PVH',
'QRVO',
'PWR',
'QCOM',
'DGX',
'RL',
'RJF',

'O',
'REG',
'REGN',
'RF',
'RSG',
'RMD',
'RHI',
'ROK',
'ROL',
'ROP',
'ROST',
'RCL',
'SPGI',
'CRM',
'SBAC',
'SLB',
'STX',
'SEE',
'SRE',
'NOW',
'SHW',
'SPG',
'SWKS',
'SLG',
'SNA',
'SO',
'LUV',
'SWK',
'SBUX',
'STT',
'STE',
'SYK',
'SIVB',
'SYF',
'SNPS',
'SYY',
'TMUS',
'TROW',
'TTWO',
'TPR',
'TGT',
'TEL',
'FTI',
'TFX',
'TXN',
'TXT',
'TMO',

'TJX',
'TSCO',
'TDG',
'TRV',
'TFC',

'TSN',
'UDR',
'ULTA',
'USB',
'UAA',
'UA',
'UNP',
'UAL',
'UNH',
'UPS',
'URI',

'UHS',
'UNM',
'VFC',
'VLO',

'VTR',
'VRSN',
'VRSK',
'VZ',
'VRTX',

'V',
'VNO',
'VMC',
'WRB',
'WAB',
'WMT',
'WBA',
'DIS',
'WM',
'WAT',
'WEC',

'WFC',
'WELL',
'WDC',
'WU',
'WRK',
'WY',
'WHR',
'WMB',

'WYNN',
'XEL',
'XRX',

'XYL',
'YUM',
'ZBRA',
'ZBH',
'ZION',
'ZTS']


final=[]
negafinal=[]
posifinal=[]
All_frames=[]
final_50pp=[]
final_50p=[]
final_137p=[]
volume_50k=[]
volume_100k=[]
volume_200k=[]
final_100p=[]
data14=[]
signal="buytime"
trade="trade"
interval=30
tradelist=[]


for ticker in Tickers:


        print('****************************************************************')
        print(f'working on {ticker} now:')
        print('****************************************************************')
        ratios = [0,0.236, 0.382, 0.5 , 0.618, 0.786,1,1.23,1.38,1.5,1.62,1.78,2]
        
        
        
        
        
        
       
        data12 = yf.download(ticker,
                             start="2022-11-14", end="2022-11-29",
                             #period="1mo",
                             interval="5m",
                             prepost=True, asynchronous=True, retry=20, status_forcelist=[404, 429, 500, 502, 503, 504])
        #start="2021-11-22", end="2021-11-27
        #start="2021-11-25", end="2021-12-03"
        #period="1m"
        data12['Symbol'] = ticker
       #=========volatility===========================================================
        Alength=0
        effectiveLen=math.ceil((Alength+1)/2)
       
        stock = finvizfinance(ticker)
        stock_fundament = stock.ticker_fundament()
        stock_fundament.pop('EPS this Y')
        stock_fundament.pop('Beta')
        stock_fundament.pop('Book/sh')
        stock_fundament.pop('Current Ratio')
        stock_fundament.pop('Dividend')
        stock_fundament.pop('Dividend %')
        stock_fundament.pop('Earnings')
        stock_fundament.pop('Employees')
        stock_fundament.pop('EPS (ttm)')
        stock_fundament.pop('EPS Q/Q')
        stock_fundament.pop('Forward P/E')
        stock_fundament.pop('Gross Margin')
        stock_fundament.pop('Income')
        stock_fundament.pop('Index')
        stock_fundament.pop('Industry')
        stock_fundament.pop('LT Debt/Eq')
        stock_fundament.pop('Oper. Margin')
        stock_fundament.pop('P/B')
        stock_fundament.pop('P/C')
        stock_fundament.pop('P/E')
        stock_fundament.pop('P/FCF')
        stock_fundament.pop('P/S')
        stock_fundament.pop('Payout')
        stock_fundament.pop('PEG')
        stock_fundament.pop('Perf Half Y')
        stock_fundament.pop('Perf Quarter')
        stock_fundament.pop('Perf Week')
        stock_fundament.pop('Perf Year')
        stock_fundament.pop('Perf YTD')
        stock_fundament.pop('Prev Close')
        stock_fundament.pop('Profit Margin')
        stock_fundament.pop('Quick Ratio')
        stock_fundament.pop('Recom')
        stock_fundament.pop('Rel Volume')
        stock_fundament.pop('ROA')
        stock_fundament.pop('ROE')
        stock_fundament.pop('ROI')
        stock_fundament.pop('Sales')
        stock_fundament.pop('Sector')
        #stock_fundament.pop('Short Ratio')
        stock_fundament.pop('Sales past 5Y')
        stock_fundament.pop('Sales Q/Q')
        
        stock_fundament.pop('EPS next 5Y')
        stock_fundament.pop('EPS next Q')
        stock_fundament.pop('EPS next Y')
        stock_fundament.pop('EPS past 5Y')
        stock_fundament.pop('52W High')
        stock_fundament.pop('52W Low')
        stock_fundament.pop('ATR')
        stock_fundament.pop('Debt/Eq')
        stock_fundament.pop('RSI (14)')
        data12["Float"]=stock_fundament['Shs Float']
        
       # data12["Shares"]=stock_fundament['Shs Outstand']
        
        #SMA this is an issue for me as this shows up as percentage string , i need to convert it to number via 
        #multiplying the value by the df["Close"] as the three criteria i intend to interweave to determine buy 
        #or sell will be the fibonacci, SMA and my third one multiplication
        #data12["SMA20"]=(stock_fundament['SMA20'])
        #data12["SMA50"]=stock_fundament['SMA50']
        #data12["SMA200"]=stock_fundament['SMA200']
        #data12["Don"]=data12["Low"].pct_change()*100
        data12['Average']=(data12['High']+data12['Low'])/2
        data12['volatile']=data12['High']+data12['Low']+data12['Close']+data12['Open']
        data12['volatile']=round(np.tan(data12['volatile'].astype(float)),2)
        #data12["p"]=data12["Close"].pct_change()*100
        sma = data12['Average'].rolling(5,min_periods=5).max().shift(1)
        data12["currentprice"]=data12["Close"][-1]
        std = data12['Close'].rolling(35,min_periods = 20).std()
        data12['upper_bb'] = sma + (std * 2)
        data12['lower_bb'] = sma - (std * 2)
        data12['profit']= data12["currentprice"]-data12['upper_bb']
        
      
        
        data12['Min']=data12['Close'].min()
        data12['Max']=data12['Close'].max()
        lowest = data12['Low'].rolling(35,min_periods = 35).mean()
        highest=data12['High'].rolling(35,min_periods = 35).mean()
        #data12['change']=( highest- lowest)*100/lowest
        data12['track']=(data12['Close']-data12['Min'])*100/data12['Min']
        #data12['Check']=((data12.Close[-1:])-(min(data12.Close)))*100/(min(data12.Close))
        data12['t-1']=data12['track'].shift(-1)
        #data12['Sell']=data12['signal'].apply(lambda x:'true' if (data12['signal']==buy, else "False")
        Low=data12["Close"].min()
        High=data12["Close"].max()
        
         #fibonnacci sequence
        Diff=High-Low
        data12["fib100"]=High
        data12["fib764"]=Low+(Diff*0.764)
        data12["Fib618"]=Low+(Diff*0.618)
        data12["Fib50"]=Low+(Diff*0.5)
        data12["Fib382"]=Low+(Diff*0.382)
        data12["Fib236"]=Low+(Diff*0.236)
       
        
       
        data12["Tr"]=data12["fib764"]- data12["currentprice"]
        data12['Buy1']=0.95*data12["Close"]
        data12['Buy2']=((data12["Low"][0:-5]).min())*1.025
        data12['Sellprice']=((data12["Close"]*1.3)-0.02)
       # data12["profit"]=(data12['Sellprice']-data12['Buy1'])*100/data12['Buy1']
       # data12["profit2"]= (data12["Fib236"]-data12['Buy2'])*100/data12['Buy2']
        #data12['Sellprice2']=((data12["Close"]*1.2)-0.02)
        #data12.loc[(data12['track']<10) & (data12['t-1']>10),'signal']='buy stock/Call'
        #data12.loc[(data12['track']>10) & (data12['t-1']<10),'signal']='Short/buy put'
        data12.loc[data12['track']<1,'signal']='Buy'
        #data12["Status"]=((1+(data12["profit"]/100))*data12['Buy1'])-data12["High"]
        #data12["sell_Stat"]=data12['Sellprice']-data12["High"]
        
        trade=pd.DataFrame((data12.loc[lambda data12:data12['signal']=='Buy', :]))
        tradelist.append(trade)
        trade_listfinal=pd.concat(tradelist)
        
       ## chker_result_df=trade_listfinal
        #if len(chker_result_df)!=0:
        #    for i in range(len(chker_result_df)):
       #      chk_date=chker_result_df.index.values
        
         #    chk_reqid=chker_result_df["Symbol"].iloc[i]
        
       # bot_message=f"Älert!!!;DATE:{chk_date};ID:{chk_reqid}"
       # bot.sendMessage(1313067608,bot_message)
       
        
        
       
       
        
        volume=data12.loc[lambda data12:data12['Volume']>1000000,:]
        volume_50k.append(volume)
        finalvolume=pd.concat(volume_50k)        
        final.append(data12)
        final2=pd.concat(final)
        Pfinalvolatile=pd.DataFrame((final2.loc[lambda final2: final2['volatile']>=50, :]))
        Nfinalvolatile=pd.DataFrame((final2.loc[lambda final2: final2['volatile']<=-50, :]))
        All_frames.append( Pfinalvolatile)
        All_frames.append( Nfinalvolatile)
        Allfinal=pd.concat(All_frames)
       

