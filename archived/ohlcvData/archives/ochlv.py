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
from time import time, sleep
import datetime
from tqdm import tqdm
import math
from finvizfinance.quote import finvizfinance

from functools import reduce      
#from ta.trend import ADXIndicator-
#rom ta import add_all_ta_features
#from ta.utils import dropna


from datetime import datetime
import matplotlib.pyplot as plt
import argparse
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicator as btind


import math


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def get_tickerlst():
    #waiting code
    mylst = ["acon","adxn","aehl","ahg"]
    #Tickers=["acon","adxn","aehl","ahg","aihs","akan","alf","allr","apm","areb","aust","baos","blbx","brezr","bsfc","cead","cnxa","crkn","ctib","cuen","drma","drug","duo","edbl","eeiq","efoi","evk","hils","htcr","htgm","imte","ipdn","ivda","jcse","jzxn","kuke","lgmk","lixt","lmfa","meds","msgm","msn","nvfy","olb","ost","phcf","prfx","pt","pte","rvsn","sdpi","snmp","sprc","sql","ssy","sxtc","tirx","ufab","uncy","vedu","vlon","vrpx","wbev","wlds","worx","xelb"]
    #Tickers=["brqs"]
    #Tickers=["fnhc","alf","acor","areb","vlon","efoi","PT","AEHL","EDBL","CTIB","NVFY","SXTC","IMTE","DUO","PTE","ALLR","ADXN","BAOS","ACON","SSY","AIHS","MEDS","LGMK","SPRC","CEAD","ensc"]
    #Tickers=["fnhc","bntc","areb","syta","muln","czoo","vstm","xela","ruby","hgen","dave","pshg","phas","cei","smts","hexo","op","snes","akba","cfms","ghsi","nuwe","nile","ubx","ccnc","stab","atnx","anpc","btb","sesn","cosm","ortx","bbln","asxc","pstv","lci","rdhl","vtgn","trvn","pbla","qtnt","wint"]
    #Tickers=["bxrx",'bntc','pte','cyto','anpc','vs','fnhc','east','krbp','vino','viri','evok','imh','yvr','grom','phio','lgmk','xbio','itp','nept','nuze','svvc','sasi','mind','taop','ptpi','wisa','nspr','imnn','kbnt','qumu','elys','lmfa','slno','mfh','otrk','bkyi','rmti','gnln','bioc','lmnl','cycc','liqt','ocg','ttnp','vvpr','imbi','game','sqft','ebet','ards','invo','apdn','nnvc','kzia','oncs','ymtx','bq','gene','wkey','dxyn','moxc','ensv','athx','hyre','hall','vvos','wavd','ekso','gray','mrai','mrin','dtea','leju','fbrx','acer','agri','nmtc','rave','bsqr','pypd','sgbx','trib','stkh','bfri','uihc','arav','rgls','wksp','wtt','clps','corr','glbs','reun','alr','dogz','nvve','lylt','cgrn','bttr','dmac','rfl','bysi','bttx','usio','tcon','awre','snt','sypr','amam','slnh','dnay','sdig','sieb','bdsx','gree']
    #Tickers=["brqs",'jwel','acon','mrai','sasi','pte','uihc','vvpr','invo','beat','lgmk','dxyn','alr','trib','rave','bfri','sxtc','tivc','sabs','edbl','sppi','hall']
    #Options ticker
    #Tickers=['adtx',"stkh","leju","envb","nbrv","pei","utsi","evok",'qngy',"wkey","bbai",'pte','cala','aezs','abeo','srga','sos','amam','slgl','avct','svvc','gnln','petz','nept',
        #   'slno',"nhtc","imnn","bntc","bpth","tzoo","rev","nspr","avtx","bkyi","lsta","ugro","wyy","daio","CMCM","cpix",'fthm','aprn','bttx','dlpn','reun','vrar','dcth','neon',
        #   'onvo','kins','ymtx',"lgmk","husa","acxp","ganx","clps","casi",'ntwk',"ltrn","gtim","fkwl","xgn","tact","achv","cpsh","rmti","lmfa","mtbc","cxdo","nmrd","sgbx","imnm","rfl","htoo",
        #   "mrai","ktcc","wimi","sieb","sasi","Taop","armp","kbnt","ITP","ensv","invo","ttnp","culp","nnvc","caas","agri","ltbr","lmnl","mfh","nyc",'srt',"rail","vvpr","ebet",
         # "sqft","apt","flux","kirk","sypr","lfvn","isun","irix","athx","icd","thrn","pcyg","ekso","cycc","feng","bmra","imh","kzia","grow","bcda","evtv"]
    return mylst

def get_ohlcv_data(mylst, startdate = "2022-4-1", enddate = "2022-10-22"):
    """
    function for getting raw ochlv data from yf
    """
    Tickers=mylst

    #initialise variables
    pd_lst = [] 

    #download ticker data from yfinance    
    for ticker in Tickers:
        print('****************************************************************')
        print(f'working on {ticker} now:')
        print('****************************************************************')
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
    df = pd.concat(pd_lst)
    return df

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
        stock_fundament_dct.pop('Short Ratio')
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

def filter_trade_signals(raw_df):
    #Filter Main Trade Summary from Data Dataframe
    trade_list=pd.DataFrame((raw_df.loc[lambda raw_df:raw_df['signal']=='buy', :]))
    return trade_list 


def get_lst_uniq_ticker_df(raw_df):
    ticker_lst = raw_df.Symbol.unique().tolist()
    df_ticker_lst = []
    for ticker in ticker_lst:
        df_tmp = pd.DataFrame((raw_df.loc[lambda raw_df:raw_df['Symbol']==ticker, :]))
        df_ticker_lst.append(df_tmp)
    return ticker_lst, df_ticker_lst

class AccountLog():
    """this class stores logs of value state/action/transactions"""
    def __init__(self):
        self.log_close         = []
        self.log_buy_executed  = []
        self.log_sell_executed = []
        self.log_buy_create    = []
        self.log_sell_create   = []
        self.log_order_cancel_reject_marg   = []
        self.log_PortfolioValue= []
        self.log_operation_profit= []
        
    
    def logprint(self):
        pass
        
class VolatileIndicator(bt.Indicator):
    lines = ('volatile','max','min')  # output line (array)
    params = (
        ('period', 1),  # distance to previous data point
        ('divfactor', 0),  # factor to use for the division
    )
    def __init__(self):
        self.volatile_not_transformed = self.data.high + self.data.low + self.data.close + self.data.open
        
        
    def __next__(self):
        sum_volatile = self.data.high[0] + self.data.low[0] + self.data.close[0] + self.data.open[0] 
        self.lines.volatile[0] = round(math.tan(float(sum_volatile)),2)


        #data_buflength = self.dataclose.buflen() #reports the total number of bars which have been loaded for the Data Feed
        data_length = len(self) #reports how many bars have been processed
        print(f'datalen:{data_length}')
        if data_length ==0:
            self.lines.min[0] = self.dataclose[0]
            self.lines.max[0] = self.dataclose[0]
        else:
            print(f'fuck shit{self.data_Min[-1]}')
            self.lines.min[0] = min(self.dataclose[0], self.data_Min[0])
            self.lines.max[0] = max(self.dataclose[0], self.data_Max[0])        
        
class TradeStrategy(bt.Strategy):
    def log(self, txt, dt=None, logItem = []):
        """logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        logentry=f'{dt.isoformat()}, {txt}'
        print(logentry)
        #this entry is useless for now
        logItem.append(logentry)

    def __init__(self):
        #this entry is useless for now
        self.logLst = AccountLog()
        
        """keep a reference to the "close" line in the data[0] dataseries"""
        #basic columns:
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        
        self.dataaverage  = (self.datahigh + self.datalow)/2
        self.ind_volatile = VolatileIndicator()
        
        # Add Bollinger bands
        #sma = data['Average'].rolling(5,min_periods=5).max().shift(1)
        #std = data['Close'].rolling(35,min_periods = 20).std()
        #data['upper_bb'] = sma + (std * 2)
        #data['lower_bb'] = sma - (std * 2)
        #data['dbb']=data['upper_bb']-data['lower_bb']
        self.data_sma = bt.indicators.SimpleMovingAverage(self.dataaverage, period=5)
        self.data_std = bt.indicators.StandardDeviation(self.dataclose, period=20)
        self.BB = bt.indicators.BollingerBands(period=21, devfactor=2.0, movav=bt.ind.MovAv.Simple)
        self.lines.topband = self.BB.top
        self.lines.botband = self.BB.bot
        self.dbb = self.lines.topband - self.lines.botband

        ##min and max columns add:
        #data['Min']=data['Close'].min()
        #data['Max']=data['Close'].max()  

        

        
         
        ##change, track,, t-1 columns add:
        #lowest = data['Low'].rolling(35,min_periods = 35).mean()
        #highest=data['High'].rolling(35,min_periods = 35).mean()
        #data['change']=( highest- lowest)*100/lowest
        #data['track']=(data['High']-data['Min'])*100/data['Min']
        #data['t-1']=data['track'].shift(-1)
        
    #
        ##Buy1 and Buy2, Sellprice1 and Sellprice2 columns add:
        #data['Buy1']=0.93*data["Close"]
        #data['Buy2']=0.95*data["Close"]
        #data['Sellprice1']=((data["Close"]*1.3)-0.02)
        #data['Sellprice2']=((data["Close"]*1.2)-0.02)   
    #
        ##Buysignals (Buy or Wait) columns add:
        #data.loc[(data['track']<10) & (data['t-1']>10),'signal']='buy'
        #data.loc[data['track']>10,'signal']='wait'         
    #
        ##fibonnacci sequence columns add:
        #Low=data["Close"].min()
        #High=data["Close"].max()
        #Diff=High-Low
        #data["fib100"]=High
        #data["fib764"]=Low+(Diff*0.764)
        #data["Fib618"]=Low+(Diff*0.618)
        #data["Fib50"]=Low+(Diff*0.5)
        #data["Fib382"]=Low+(Diff*0.382)
        #data["Fib236"]=Low+(Diff*0.236)
        #data["Fib0"]=Low    
        #return data
        
        
        #keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def next(self):
        ##simply log the closing price of the series from the reference
        #self.log(f'Close, {self.dataclose[0]:.2f}', self.logLst.log_close)
        


        #simply log the closing price of the series from the reference


        #main strategy
        #Check if an order is pending....if yes we cant send a 2nd order
        if self.order:
            return
        #Check if we are in the market and buy conditions!!!!
        if not self.position:
            # afolabi: pls provide a description of this conditions
            if ((self.dataclose[0] - min(self.dataclose))*100/min(self.dataclose))>10:
                # afolabi: pls provide a description of this conditions
                if ((self.dataclose[-1] - min(self.dataclose))*100/min(self.dataclose))<10: 
                    # BUY CONDITION WITH ALL POSSIBLE PARAMETERS PASSED!!!!
                    self.log(f'BUY CREATE, {self.dataclose[0]}', self.logLst.log_buy_create)
                    #Keep track of the created order to avoid a second order
                    self.order=self.buy()

        else:
            # Already in the market.....we might sell and sell conditions


          # # if self.dataclose[0] >=data1["Sellprice1"][0]:
          #     if data1["signal"][0]=="Sell":
          #        self.dataclose==((data1["fib100"]))          (this code is meant to be the sell condition , however i am still trying to figure out it out , its meant to be 1.3* price of the above buy indicator)            
            
            
            if len(self)>(self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log(f'SELL CREATE, {self.dataclose[0]}', self.logLst.log_sell_create)
                # Keep Track of the created order in order to avoid a 2nd order
                self.order=self.sell()
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            #Buy/Sell order submitted/accepted to/by broker-Nothing to do
            return
        #Check if an order has been completed
        #Attention:Broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}|Cost: {order.executed.value:.2f}|Comm: {order.executed.comm:.2f}', self.logLst.log_buy_executed)
                self.buyprice = order.executed.price
                self.buycomm  = order.executed.comm
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}|Cost: {order.executed.value:.2f}|Comm: {order.executed.comm:.2f}', self.logLst.log_buy_executed)
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected', self.logLst.log_order_cancel_reject_marg )
            #Write down:no pending order
            self.order=None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'OPERATION PROFIT, GROSS: {trade.pnl:.2f}, NET: {trade.pnlcomm}', self.logLst.log_operation_profit)
    

                
def backtest(raw_df):
    #Instantiate Cerebro engine
    cerebro = bt.Cerebro(stdstats=False)

    #run operations on each unique ticker
    #Add strategy to Cerebro
    cerebro.addstrategy(TradeStrategy) 

    #add ochlv data to cerebro
    ticker_lst, df_ticker_lst = get_lst_uniq_ticker_df(raw_df)

 
        
    for ticker, ticker_df in zip(ticker_lst, df_ticker_lst):


        # Pass dataframe to the backtrader datafeed and add it to the cerebro    
        data =  bt.feeds.PandasData(dataname = ticker_df,
                                    #datetime = 'Date',
                                    nocase=True,
                                    )
        cerebro.adddata(data) 
        cerebro.broker.setcash(100000) # You can type 10000 as a beginning cash
        cerebro.broker.setcommission(commission=0.001) # You can change the commission rate

        #print out starting conditions for each ticker
        print(f'Starting Portfolio Value for {ticker}: {cerebro.broker.getvalue():.2f}')
        
        #Run Cerebro Engine
        cerebro.run()

        #print out final results for each ticker
        print(f'Final Portfolio Value for {ticker}: {cerebro.broker.getvalue():.2f}')
        
    #Plot the resultCerebro Engine
    #cerebro.plot(style='bar')
    cerebro.plot()
    #cerebro.plot(style='candlestick',loc='grey', grid=False)

def main():
    tickerlst = get_tickerlst()
    raw_df = get_ohlcv_data(tickerlst)
    trade_list = filter_trade_signals(raw_df)

    # outputing relevant dataframes to excel file
    #afolabi.query|start|you can change the location of your output file to a folder on your computer?????   
    outputfile = r'C:\Users\ROSEMARY\Downloads\akt.files\apps.files\git.files\ohlcvData\outputs\Output.xlsx' #home
    #outputfile = r'C:\Users\akintunde.adegbayo\Downloads\test\Output.xlsx' #office
    with pd.ExcelWriter(outputfile) as writer:  
        raw_df.to_excel(writer, sheet_name='AllData')
        trade_list.to_excel(writer, sheet_name='TradeList')
    
    backtest(raw_df)
    


if __name__ == "__main__":
    main()

