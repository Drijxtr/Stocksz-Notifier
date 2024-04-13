import sys
import yfinance as yf
import pandas as pd
import os
os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1')
import re


class Listed_watchlist():
    def __init__(self):
            try:
                if os.path.exists("watchlist.csv"):
                    self.df = pd.read_csv("watchlist.csv")
                    column_x = ['Name', 'LTP', 'Alert_price', 'Volume', 'Daily %', 'Exchange','Currency']
                    if self.df.columns.all() != column_x :
                        pass
                    else:
                        raise pd.errors.EmptyDataError
            except pd.errors.EmptyDataError:
                print("watchlist.csv is empty or is mismatched. Recreating DataFrame.")
                self.df = pd.DataFrame(columns=["Name", "LTP", "Alert_price", "Volume", "Daily %","Exchange", "Currency"])
                self.df.to_csv("watchlist.csv", index=False)
                
    def watchlist_stocks(self):
        if self.df.empty:
            pass
        else:
            print(self.df)
            
    
    def watchlist_edit(self,stock):
        self.w_stock= stock
        previous_Close, price_cur = map(int , [stock["previousClose"], stock["currentPrice"]])
        change_per= ((price_cur- previous_Close )/previous_Close)*100
        change_per= f"{change_per:.2f}"
        self.new_data= {"Name": [stock["shortName"].upper()],
                        "Symbol": [stock["symbol"]],
                        "LTP": [stock["currentPrice"]],
                        "Alert_price": [599],
                        "Volume": [stock["volume"]],
                        "Daily %": [f"{change_per}%"],
                        "Currency": [stock["financialCurrency"]],
                        "Exchange": [stock["exchange"]]
                        }
        if self.df.empty:
            self.df = pd.DataFrame(self.new_data)
        else:
            self.df = pd.concat([self.df, pd.DataFrame(self.new_data)])
        self.df.to_csv("watchlist.csv", index=False)
        self.df.index= self.df.index+1
        self.df.reset_index(drop=True, inplace=True)
        return print(pd.DataFrame(self.df["Name"]))

    def Add_stocks(self):
        watchlist_edit_menus= f"Commands: {"ALERT", "BACK", "EXIT"}"
        while True:
            print(watchlist_edit_menus, end="\n\n")
            self.watchlist_stocks()
            print("Type the stock's symbol to add", end="\n\n")
            add_req= input("__").upper()
            if add_req == "BACK":
                return
            if add_req == "EXIT":
                sys.exit("Shutting script")
            try:
                stocks_info= yf.Ticker(add_req).info
                if not stocks_info:
                    raise Exception
                else:
                    print("fsdf")
                    self.watchlist_edit(stocks_info)
                    continue
                op
            except Exception as e:
                print("Invalid symbol, please check again")
                pass
    def Remove_stocks(self):
        watchlist_remove_menus= f"Commands: {"BACK", "EXIT"}"
        while True:
            print(watchlist_remove_menus)
            self.watchlist_stocks()
            print("Type the stock's symbol/name/number to remove")
            remove_req= input("").upper()
            if remove_req == "BACK" or remove_req == "EXIT":
                if remove_req == "BACK":
                    break
                elif remove_req == "EXIT":
                    sys.exit("Shutting script")
            else:
                rem_condition = (self.df["Symbol"] == remove_req) | (self.df["Name"] == remove_req)
                if rem_condition.any():
                    self.df= self.df[-rem_condition]
                    self.df.to_csv("watchlist.csv", index=False)
                    self.watchlist_stocks
                    continue
                else:
                    print(f"{remove_req} didn't matched any stock symbol or name check again")    
                      
    def stockAlert(self):
        watchlist_alert_menus= f"Commands: {"BACK", "EXIT"}"
        while True:
            print(watchlist_alert_menus)
            self.watchlist_stocks()
            print("Type the stock's symbol/name/number to remove")
            alert_req= input("_")

            if alert_req== "BACK" or alert_req== "EXIT":
                if alert_req == "BACK":
                    break
                else:
                    sys.exit("Shutting scripts")
            try:
                alert_condition= (self.df["Symbol"] == alert_req | (self.df["Name"] == alert_req))
                if alert_condition.any():
                    alert_val= float(input(""))
                    self.df= self.df{"Name":[] [alert_val]
                    self.df.to_csv("watchlist.csv", index=False)
                    self.watchlist_stocks
                   # print("Type a value to set alert")
                    
                    continue
                else:
                    print(f"{alert_req} didn't matched any stock symbol or name check again")
            except ValueError:
                print(f"{alert_req} is not a valid value!")
                raise
            
        
def main():
    Interface()

def Interface():
    valid_menus= f"Commands: {"INFO", "EDIT", "LTP"}"
    while True or req == "exit":
        print(valid_menus)
        req = input("_ ").upper()
        #req= "edit"
        if valid_menus in req:
            print("Invalid command")
        Req_handler(req)

def Req_handler(req):
    if req == "EXIT":
        return sys.exit("X")
    if req == "TEST":
        x3= Listed_watchlist()
        x3.watchlist_stocks()
        return

    if req == "INFO":
        my_watchlist= Listed_watchlist()
        for stocks in my_watchlist:
            x1= my_watchlist.Watchlisted()
        tickers= yf.Ticker("MSFT").info

    if req == "LTP":
        watchlist()
    if req == "EDIT":
        watchlist_modify()

def watchlist():
    msft = yf.Ticker("MSfFT").info
    ltp =msft["currentPrice"]
    print(ltp)
    sys.exit()

def watchlist_modify():
    my_watchlist = Listed_watchlist()
    print("Modifying watchlist")
    watchlist_edit_menus= f"Commands: {"ADD", "ALERT", "REMOVE", "LTP", "BACK", "EXIT"}"
    while True:
        print(watchlist_edit_menus)
        w_modify_req= input("_").upper()
        #print(end= "\n"+"\n")
        if w_modify_req == "EXIT":
            sys.exit("Shutting script")
        if w_modify_req == "ADD":
            my_watchlist.Add_stocks()
        if w_modify_req == "ALERT":
            my_watchlist.stockAlert()
        if w_modify_req == "REMOVE":
            my_watchlist.Remove_stocks()

def Sys_handler():
    ...

if __name__ == "__main__":
    main()
