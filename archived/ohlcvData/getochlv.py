# -*- coding: utf-8 -*-
"""
modified on Wed Oct 26 2022 @author: Akt
modified on Sat Oct 22 14:01:52 2022 @author: afolabi
modified on Sun Oct  9 17:51:30 2022 @author: afola
Created on Thu Oct  6 18:55:55 2022 @author: afola
"""

from __future__ import (absolute_import, division, print_function,unicode_literals)
import yfinance as yf
import pandas as pd
import numpy as np
from finvizfinance.quote import finvizfinance
import math

# from time import time, sleep
# import datetime
# from tqdm import tqdm
# import math

# 
# from functools import reduce      
# #from ta.trend import ADXIndicator-
# #rom ta import add_all_ta_features
# #from ta.utils import dropna
# 
# 
# from datetime import datetime
# import matplotlib.pyplot as plt
# import argparse
# import backtrader as bt
# import backtrader.feeds as btfeeds
# import backtrader.indicator as btind
# 
# 



pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def get_finvizfinance_data(ticker, data):
        stock = finvizfinance(ticker)
        
        stock_fundament_dct = stock.ticker_fundament() # this is a series or dict oga!!!!!

        stock_fundament_dct.pop('EPS this Y')
        stock_fundament_dct.pop('Beta')
        stock_fundament_dct.pop('Book/sh')
        stock_fundament_dct.pop('Current Ratio')
        stock_fundament_dct.pop('Dividend')
        stock_fundament_dct.pop('Dividend %')
        stock_fundament_dct.pop('Earnings')
        stock_fundament_dct.pop('Employees')
        stock_fundament_dct.pop('EPS (ttm)')
        stock_fundament_dct.pop('EPS Q/Q')
        stock_fundament_dct.pop('Forward P/E')
        stock_fundament_dct.pop('Gross Margin')
        stock_fundament_dct.pop('Income')
        stock_fundament_dct.pop('Index')
        stock_fundament_dct.pop('Industry')
        stock_fundament_dct.pop('LT Debt/Eq')
        stock_fundament_dct.pop('Oper. Margin')
        stock_fundament_dct.pop('P/B')
        stock_fundament_dct.pop('P/C')
        stock_fundament_dct.pop('P/E')
        stock_fundament_dct.pop('P/FCF')
        stock_fundament_dct.pop('P/S')
        stock_fundament_dct.pop('Payout')
        stock_fundament_dct.pop('PEG')
        stock_fundament_dct.pop('Perf Half Y')
        stock_fundament_dct.pop('Perf Quarter')
        stock_fundament_dct.pop('Perf Week')
        stock_fundament_dct.pop('Perf Year')
        stock_fundament_dct.pop('Perf YTD')
        stock_fundament_dct.pop('Prev Close')
        stock_fundament_dct.pop('Profit Margin')
        stock_fundament_dct.pop('Quick Ratio')
        stock_fundament_dct.pop('Recom')
        stock_fundament_dct.pop('Rel Volume')
        stock_fundament_dct.pop('ROA')
        stock_fundament_dct.pop('ROE')
        stock_fundament_dct.pop('ROI')
        stock_fundament_dct.pop('Sales')
        stock_fundament_dct.pop('Sector')
#        stock_fundament_dct.pop('Short Ratio') this isnt working!!!!!
        stock_fundament_dct.pop('Sales past 5Y')
        stock_fundament_dct.pop('Sales Q/Q')

        stock_fundament_dct.pop('EPS next 5Y')
        stock_fundament_dct.pop('EPS next Q')
        stock_fundament_dct.pop('EPS next Y')
        stock_fundament_dct.pop('EPS past 5Y')
        stock_fundament_dct.pop('52W High')
        stock_fundament_dct.pop('52W Low')
        stock_fundament_dct.pop('ATR')
        stock_fundament_dct.pop('Debt/Eq')
        stock_fundament_dct.pop('RSI (14)')
        # stock_fundament_dct.pop('Volatility W')
        data["Float"]=stock_fundament_dct['Shs Float']
        data["Shares"]=stock_fundament_dct['Shs Outstand']

        #afolabi.query|start|this sma values seem wrong. there is only a single value per ticker regardless of timeframe
        # i thought it changes over time?????    
        #SMA this is an issue for me as this shows up as percentage string , i need to convert it to number via 
        #multiplying the value by the df["Close"] as the three criteria i intend to interweave to determine buy 
        #or sell will be the fibonacci, SMA and my third one multiplication
        stock_fundament_dct['SMA20'] = float(stock_fundament_dct['SMA20'].replace('%',''))
        stock_fundament_dct['SMA50'] = float(stock_fundament_dct['SMA50'].replace('%',''))
        stock_fundament_dct['SMA200'] = float(stock_fundament_dct['SMA200'].replace('%',''))        

        data["SMA20"] = stock_fundament_dct['SMA20'] * data['Close'] / 100
        data["SMA50"] = stock_fundament_dct['SMA50'] * data['Close'] / 100  
        data["SMA200"]= stock_fundament_dct['SMA200'] * data['Close'] / 100
        #afolabi.query|end|------------------------------------------
        return data
def add_ohlcv_columns(data):
    #volatility column add:
    #afolabi.query|start|what are this 2 lines doing. its not referenced anywhere?????
    Alength=0
    effectiveLen=math.ceil((Alength+1)/2)
    #afolabi.query|end|------------------------------------------

    data['Average']=(data['High']+data['Low'])/2
    data['volatile']=data['High']+data['Low']+data['Close']+data['Open']
    data['volatile']=round(np.tan(data['volatile'].astype(float)),2)

    #bollinger bands columns add:
    sma = data['Average'].rolling(5,min_periods=5).max().shift(1)
    std = data['Close'].rolling(35,min_periods = 20).std()
    data['upper_bb'] = sma + (std * 2)
    data['lower_bb'] = sma - (std * 2)
    data['dbb']=data['upper_bb']-data['lower_bb']

    #min and max columns add:
    data['Min']=data['Close'].min()
    data['Max']=data['Close'].max()    

    #change, track,, t-1 columns add:
    lowest = data['Low'].rolling(35,min_periods = 35).mean()
    highest=data['High'].rolling(35,min_periods = 35).mean()
    data['change']=( highest- lowest)*100/lowest
    data['track']=(data['High']-data['Min'])*100/data['Min']
    data['t-1']=data['track'].shift(-1)

    #Buy1 and Buy2, Sellprice1 and Sellprice2 columns add:
    data['Buy1']=0.93*data["Close"]
    data['Buy2']=0.95*data["Close"]
    data['Sellprice1']=((data["Close"]*1.3)-0.02)
    data['Sellprice2']=((data["Close"]*1.2)-0.02)   

    #Buysignals (Buy or Wait) columns add:
    data.loc[(data['track']<10) & (data['t-1']>10),'signal']='buy'
    data.loc[data['track']>10,'signal']='wait'         

    #fibonnacci sequence columns add:
    Low=data["Close"].min()
    High=data["Close"].max()
    Diff=High-Low
    data["fib100"]=High
    data["fib764"]=Low+(Diff*0.764)
    data["Fib618"]=Low+(Diff*0.618)
    data["Fib50"]=Low+(Diff*0.5)
    data["Fib382"]=Low+(Diff*0.382)
    data["Fib236"]=Low+(Diff*0.236)
    data["Fib0"]=Low    
    return data


def get_ohlcv_data(mylst, startdate = "2022-4-1", enddate = "2022-10-22"):
    """
    function for getting raw ochlv data from yf
    """
    Tickers=mylst

    #initialise variables
    pd_lst = [] 

    #download ticker data from yfinance    
    print('+' * 80)
    for ticker in Tickers:
        ratios = [0,0.236, 0.382, 0.5 , 0.618, 0.786,1,1.23,1.38,1.5,1.62,1.78,2]
        data = yf.download(ticker,
                             start=startdate, end=enddate,
                             #period="1mo",
                             interval="1h",
                             prepost=True, asynchronous=True, retry=20, status_forcelist=[404, 429, 500, 502, 503, 504])
        data['Symbol'] = ticker
        data = data.loc[:,['Symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
        data = get_finvizfinance_data(ticker, data)
        data = add_ohlcv_columns(data)
        
        pd_lst.append(data)
        print(f'data extracted for {ticker}:')                                   
    print('+' * 80)
    df = pd.concat(pd_lst)
    return df





def filter_trade_signals(raw_df):
    #Filter Main Trade Summary from Data Dataframe
    trade_list=pd.DataFrame((raw_df.loc[lambda raw_df:raw_df['signal']=='buy', :]))
    return trade_list 

def output_excel(raw_df, trade_list, outputfile ):
    with pd.ExcelWriter(outputfile) as writer:  
        raw_df.to_excel(writer, sheet_name='AllData')
        trade_list.to_excel(writer, sheet_name='TradeList')


   
def gettradelst(tickerlst):
    raw_df = get_ohlcv_data(tickerlst)
    trade_list = filter_trade_signals(raw_df) 

    # outputing relevant dataframes to excel file
    #afolabi.query|start|you can change the location of your output file to a folder on your computer?????   
    #outputfile = r'C:\Users\ROSEMARY\Downloads\akt.files\apps.files\git.files\ohlcvData\outputs\Output.xlsx' #home
    outputfile = r'C:\Users\akintunde.adegbayo\Downloads\test\Output.xlsx' #office
    output_excel(raw_df, trade_list, outputfile)
    print_output = f'output written to \n{outputfile}'

    print(f'{print_output}')
    print('+' * 80)
    
    return raw_df,trade_list

