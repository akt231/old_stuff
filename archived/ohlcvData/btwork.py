import backtrader as bt
import pandas as pd
import numpy as np

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

    print('+' * 80)         
    #Plot the resultCerebro Engine
    #cerebro.plot(style='bar')
    cerebro.plot()
    #cerebro.plot(style='candlestick',loc='grey', grid=False)
