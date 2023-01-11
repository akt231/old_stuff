import gettickers
import getochlv
import btwork

def main():                           
    tickerlst = gettickers.get_tickerlst()       
    raw_df,trade_list = getochlv.gettradelst(tickerlst)
    btwork.backtest(raw_df) 

      
    print('we are done') 
    print('+' * 80)      


if __name__ == "__main__":
    main()    