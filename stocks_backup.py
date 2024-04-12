import sys
import yfinance as yf
import pandas as pd
import os
import re

class Listed_watchlist():
    def __init__(self):    
        try:
            if os.path.exists("watchlist.csv"):
                self.df = pd.read_csv("watchlist.csv")
            else:
                self.df = pd.DataFrame(columns=["Name", "LTP", "Alert_price", "Volume", "Daily %", "Currency"])
                self.df.to_csv("watchlist.csv", index= False)
        except pd.errors.EmptyDataError:
            print("watchlist.csv is empty or has no columns. Creating a new DataFrame.")
            self.df = pd.DataFrame(columns=["Name", "LTP", "Alert_price", "Volume", "Daily %", "Currency"])
            
            
            
    def watchlist_stocks(self):
        print()
        print(self.df)
        print()

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
                        "exchange": [stock["exchange"]]
                        }
                    #previousClose
        if self.df.empty:
            self.df = pd.DataFrame(self.new_data)
        else:
            self.df = pd.concat([self.df, pd.DataFrame(self.new_data)])

        #self.df = pd.concat([self.df, pd.DataFrame(self.new_data)])
        self.df.to_csv("watchlist.csv", index=False)
        self.df.index= self.df.index+1
        self.df.reset_index(drop=True, inplace=True)
        return print(pd.DataFrame(self.df["Name"]))

    def Add_stocks(self):
        watchlist_edit_menus= f"Commands: {"ALERT", "BACK", "EXIT"}"
        while True:
            print(watchlist_edit_menus)
            self.watchlist_stocks()
            print("Type the stock's symbol to add")
            add_req= input("").upper()
            if add_req == "BACK":
                return
            if add_req == "EXIT":
                sys.exit("Shutting script")
            
            stocks_info= yf.Ticker(add_req).info
            try:
                if "previousClose" not in stocks_info:
                    raise KeyError
                else:
                    self.watchlist_edit(stocks_info)
                    continue
            except YFinanceException as e:
                print(e)
                print("Invalid symbol, please check again")
                pass
    def Remove_stocks(self):
        watchlist_remove_menus= f"Commands: {"BACK", "EXIT"}"
        while True:
            print(watchlist_remove_menus)
            self.watchlist_stocks
            print("Type the stock's symbol/name/number to remove")
            remove_req= input("").upper()
            rem_condition = (self.df['Symbol'] == remove_req) | (self.df['Name'] == remove_req)
            if remove_req == "BACK":
                break
            elif remove_req == "EXIT":
                sys.exit("Shutting script")
            if rem_condition.any():
                self.df= self.df[-rem_condition]
                self.df.to_csv("watchlist.csv", index=False)
                print("f")
                self.watchlist_stocks
                continue
            else:
                print(f"{rem_condition} didn't matched any stock check again")      
        
        
        
        

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
        w_modify_req= input("").upper()
        if w_modify_req == "EXIT":
            sys.exit("Shutting script")
        my_watchlist.watchlist_stocks()
        if w_modify_req == "ADD":
            my_watchlist.Add_stocks()
        if w_modify_req == "REMOVE":
            my_watchlist.Remove_stocks()

def Sys_handler():
    ...

if __name__ == "__main__":
    main()
