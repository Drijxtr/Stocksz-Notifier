import sys
import yfinance as yf
import pandas as pd
import os
import threading
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
from art import *
import cowsay
import pyttsx3

class Listed_watchlist():
    def __init__(self):
        self.engine = pyttsx3.init()
        try:
            if os.path.exists("watchlist.csv"):
                self.df = pd.read_csv("watchlist.csv")
                column_x = ['Name', 'Symbol' ,'LTP', 'Alert_con', "Alert_price",'Volume', 'Daily %','Exchange','Currency']
                if not all(col in self.df.columns for col in column_x):
                    self.df = self.df.reindex(columns=column_x)
                    raise pd.errors.EmptyDataError
            else:
                raise pd.errors.EmptyDataError
        except pd.errors.EmptyDataError:
            print("watchlist.csv is empty or is mismatched. Recreating DataFrame.")
            self.df = pd.DataFrame(columns=['Name', 'Symbol' ,'LTP', 'Alert_con', "Alert_price",'Volume', 'Daily %','Exchange','Currency'])
            self.df.to_csv("watchlist.csv", index=False)
                
    def update_stocks(self):
        if self.df.empty:
            pass
        else:
            for index, row in self.df.iterrows():
                stock_symbol= row["Symbol"]
                stock_info = yf.Ticker(stock_symbol).info
                if stock_info:
                    try:
                        previous_Close, price_cur = map(float, [stock_info["previousClose"], stock_info["currentPrice"]])
                        change_per = ((price_cur - previous_Close) / previous_Close) * 100
                        change_per= f"{change_per:.2f}"
                        change_per = float(change_per)
                    except ValueError:
                        print(f"{row['Symbol']} can't fetch all data")
                        pass
                    self.df.at[index, "LTP"] = stock_info.get("currentPrice")
                    self.df.at[index, "Volume"] = stock_info.get("volume")
                    self.df.at[index, "Daily %"] = change_per
                    self.df.to_csv("watchlist.csv", index=False)
                else:
                    print(stock_symbol)
                    print(f"Couldn't fetch data for {stock_symbol} skipping")
    def watchlist_ltp(self):
        if self.df.empty:
            print("Add stocks to the watchlist first")
        else:
            
            print(self.df)

    def watchlist_edit(self,stock):
        self.w_stock= stock
        try:
            previous_Close, price_cur = map(int , [stock["previousClose"], stock["currentPrice"]])
            change_per= ((price_cur- previous_Close )/previous_Close)*100
            change_per= f"{change_per:.2f}"
        except Exception:
            print(end="\n\n")
            print("Invalid symbol, please check again")
            return
        self.new_data= {"Name": [stock["shortName"].upper()],
                        "Symbol": [stock["symbol"]],
                        "Alert_price": [float('nan')],
                        "Alert_con": ["X"],
                        "LTP": [stock["currentPrice"]],
                        "Volume": [stock["volume"]],
                        "Daily %": [f"{change_per}%"],
                        "Currency": [stock["financialCurrency"]],
                        "Exchange": [stock["exchange"]]
                        }
        
        if self.df.empty:
            self.df = pd.DataFrame(self.new_data)
            self.df.to_csv("watchlist.csv", index= False)
            return True
        else:
            self.df = pd.concat([self.df, pd.DataFrame(self.new_data)])
            self.df.to_csv("watchlist.csv", index=False)
            self.df.index= self.df.index+1
            self.df.reset_index(drop=True, inplace=True)
            return True

    def Add_stocks(self):
        watchlist_edit_menus= f'Commands: {"ALERT", "BACK", "EXIT"}'
        while True:
            print(watchlist_edit_menus)
            self.watchlist_ltp()
            print("Type the stock's symbol to add", end="\n\n")
            add_req= input("__").upper()
            if add_req == "BACK":
                return
            elif add_req == "EXIT":
                sys.exit("Shutting script")
            stocks_info= yf.Ticker(add_req).info
            if not stocks_info:
                raise Exception
            try:
                if add_req in self.df["Symbol"].values:
                    print(f"{add_req} already exists in the watchlist")
                else:
                    self.watchlist_edit(stocks_info)
                    print(end= "\n\n")
                    continue
            except KeyError:
                    self.watchlist_edit(stocks_info)
                    print(end= "\n\n")
                    continue
    def Add_check(self,stock):
        if stock in self.df["Symbol"].values:
            print(f"{stock} already exists in the watchlist")
            sys.exit("")
        else:
            return True
    
    def Remove_stocks(self, rem_stock= "_"):
        if rem_stock== "_":
            watchlist_remove_menus= f"Commands: {"BACK", "EXIT"}"
            while True:
                print(watchlist_remove_menus)
                self.watchlist_ltp()
                print("Type the stock's symbol/name/number to remove")
                remove_req= input("").upper()
                if remove_req == "BACK" or remove_req == "EXIT":
                    if remove_req == "BACK":
                        break
                    elif remove_req == "EXIT":
                        sys.exit("Shutting script")
                rem_condition = (self.df["Symbol"] == remove_req) | (self.df["Name"] == remove_req)
                if rem_condition.any():
                    self.df= self.df[-rem_condition]
                    self.df.to_csv("watchlist.csv", index=False)
                    self.watchlist_ltp
                    continue
                else:
                    print(f"{remove_req} didn't matched any stock symbol or name check again")
        else:    
            rem_condition = (self.df["Symbol"] == rem_stock) | (self.df["Name"] == rem_stock)
            if rem_condition.any():
                self.df= self.df[-rem_condition]
                self.df.to_csv("watchlist.csv", index=False)
                self.watchlist_ltp
                sys.exit(f"Removed {rem_stock} from watchlist")
            else:
                print(f"{rem_stock} didn't matched any stock symbol or name check again")                     
                sys.exit("")
    def stockAlert(self):
        watchlist_alert_menus= f"Commands: {"BACK", "EXIT"}"
        while True:
            print(watchlist_alert_menus)
            self.watchlist_ltp()
            while True:
                print("Type the stock's symbol/name you want to set a alert for")
                alert_req= input("_").upper()
                if alert_req== "BACK" or alert_req== "EXIT":
                    if alert_req == "BACK":
                        return
                    else:
                        sys.exit("Shutting scripts")
                alert_condition= (self.df["Symbol"] == alert_req) | (self.df["Name"] == alert_req)
                if alert_condition.any():
                        while True:
                            valid_conditions= {">", ">=", "==", "<", "<="}
                            alert_instructions=f"> for greater than ltp {"\n"} >= for greater than or equal to ltp{"\n"} < for less than ltp{"\n"} <= for less than or equal to ltp{"\n"} == for equal to ltp"
                            print(alert_instructions)
                            user_alert_instructions = str(input("_ ")).upper()
                            if user_alert_instructions in valid_conditions or (user_alert_instructions== "BACK" or user_alert_instructions== "EXIT"):
                                if user_alert_instructions== "BACK" or user_alert_instructions== "EXIT":
                                    if user_alert_instructions == "BACK":
                                        break
                                    else:
                                        sys.exit("Shutting scripts")
                            else:
                                print("Invalid input. Please try again.")
                                break
                            print("Type a value to set alert")
                            try:
                                alert_val= float(input(""))
                                self.df.loc[alert_condition, "Alert_price"]= alert_val
                                print(f"{alert_req} sets the alert price to {alert_val}")
                                if user_alert_instructions == ">" and (self.df.loc[alert_condition, "LTP"] > float(alert_val)).all():
                                    alert_stock= self.df.loc[alert_condition, "Symbol"].values[0]
                                    print(f"{alert_stock} already matches the alert condition")
                                    self.df.loc[alert_condition, "Alert_price"] = float('nan')
                                    self.df.to_csv("watchlist.csv", index=False)
                                    break
                                elif user_alert_instructions == ">=" and (self.df.loc[alert_condition, "LTP"] >= float(alert_val)).all():
                                    alert_stock= self.df.loc[alert_condition, "Symbol"].values[0]
                                    print(f"{alert_stock} already matches the alert condition")
                                    self.df.loc[alert_condition, "Alert_price"] = float('nan')
                                    self.df.to_csv("watchlist.csv", index=False)
                                    break
                                elif user_alert_instructions == "==" and (self.df.loc[alert_condition, "LTP"] == float(alert_val)).all():
                                    alert_stock= self.df.loc[alert_condition, "Symbol"].values[0]
                                    print(f"{alert_stock} already matches the alert condition")
                                    self.df.loc[alert_condition, "Alert_price"] = float('nan')
                                    self.df.to_csv("watchlist.csv", index=False)
                                    break
                                elif user_alert_instructions == "<" and (self.df.loc[alert_condition, "LTP"] < float(alert_val)).all():
                                    alert_stock= self.df.loc[alert_condition, "Symbol"].values[0]
                                    print(f"{alert_stock} already matches the alert condition")
                                    self.df.loc[alert_condition, "Alert_price"] = float('nan')
                                    self.df.to_csv("watchlist.csv", index=False)
                                    break
                                elif user_alert_instructions == "<=" and (self.df.loc[alert_condition, "LTP"] <= float(alert_val)).all():
                                    alert_stock= self.df.loc[alert_condition, "Symbol"].values[0]
                                    print(f"{alert_stock} already matches the alert condition")
                                    self.df.loc[alert_condition, "Alert_price"] = float('nan')
                                    self.df.to_csv("watchlist.csv", index=False)
                                    break
                                self.df.loc[alert_condition, "Alert_con"] = user_alert_instructions
                                self.df.to_csv("watchlist.csv", index=False)
                                break
                            except ValueError:
                                print(f"Not a valid value! try again")
                                break
                else:
                    print(f"{alert_req} didn't matched any stock symbol or name check again")
                    continue            

    def alert_stock(self):
        pygame.mixer.init()
        pygame.mixer.music.load(r'C:\Users\Aditya\final_project\alert_sound.wav')
        for index,alert_values in self.df.iterrows():
            ltp = alert_values["LTP"]
            Alert_con = alert_values["Alert_con"]
            Alert_price = alert_values["Alert_price"]
            if not Alert_price == "X":
                ltp, Alert_price = map(float, [ltp, Alert_price])
                if (ltp > Alert_price) and Alert_con == ">":
                    self.df.loc[index, "Alert_con"] = "X"
                    self.df.loc[index, "Alert_price"] = float("nan")
                    self.df.to_csv("watchlist.csv", index=False)
                    print(f"ALERT!!! {alert_values["Symbol"]} REACHED {Alert_price} {alert_values["Currency"]}")
                    alerting_stock= f"ALERT!!! {alert_values["Symbol"]} REACHED {Alert_price}"
                    cowsay.cow(alerting_stock)
                    alerting_tts= f"ALERT!!! {alert_values["Name"]} TRIGGERED YOUR ALERT VALUE OF {Alert_price} {alert_values["Currency"]}"
                    self.engine.say(alerting_tts)
                    self.engine.runAndWait()
                elif (ltp >= Alert_price) and Alert_con == ">=":
                    self.df.loc[index, "Alert_con"] = "X"
                    self.df.loc[index, "Alert_price"] = float("nan")
                    self.df.to_csv("watchlist.csv", index=False)
                    print(f"ALERT!!! {alert_values["Symbol"]} REACHED {Alert_price} {alert_values["Currency"]}")
                    alerting_tts= f"ALERT!!! {alert_values["Name"]} TRIGGERED YOUR ALERT VALUE OF {Alert_price} {alert_values["Currency"]}"
                    self.engine.say(alerting_tts)
                    self.engine.runAndWait()
                elif (ltp < Alert_price) and Alert_con == "<":
                    pygame.mixer.music.play()
                    self.df.loc[index, "Alert_price"] = float("nan")
                    self.df.loc[index, "Alert_con"] = "X"
                    self.df.to_csv("watchlist.csv", index=False)
                    print(f"ALERT!!! {alert_values["Symbol"]} REACHED {Alert_price} {alert_values["Currency"]}")
                    alerting_tts= f"ALERT!!! {alert_values["Name"]} TRIGGERED YOUR ALERT VALUE OF {Alert_price} {alert_values["Currency"]}"
                    self.engine.say(alerting_tts)
                    self.engine.runAndWait()
                elif (ltp <= Alert_price) and Alert_con == "<=":
                    self.df.loc[index, "Alert_con"] = "X"
                    self.df.loc[index, "Alert_price"] = float("nan")
                    self.df.to_csv("watchlist.csv", index=False)
                    print(f"ALERT!!! {alert_values["Symbol"]} REACHED {Alert_price} {alert_values["Currency"]}")
                    pygame.mixer.music.play()
                    alerting_tts= f"ALERT!!! {alert_values["Name"]} TRIGGERED YOUR ALERT VALUE OF {Alert_price} {alert_values["Currency"]}"
                    self.engine.say(alerting_tts)
                    self.engine.runAndWait()
                elif (ltp == Alert_price) and Alert_con == "==":
                    pygame.mixer.music.play()
                    self.df.loc[index, "Alert_con"] = "X"
                    self.df.loc[index, "Alert_price"] = float("nan")
                    self.df.to_csv("watchlist.csv", index=False)
                    print(f"ALERT!!! {alert_values["Symbol"]} REACHED {Alert_price} {alert_values["Currency"]}")
                    alerting_stock= f"ALERT!!! {alert_values["Symbol"]} REACHED {Alert_price}"
                    cowsay.cow(alerting_stock)
                    alerting_tts= f"ALERT!!! {alert_values["Name"]} TRIGGERED YOUR ALERT VALUE OF {Alert_price} {alert_values["Currency"]}"
                    self.engine.say(alerting_tts)
                    self.engine.runAndWait()
            else:
                pass
    
    def updateAnd_alert(self):
        while True:
            self.update_stocks()
            self.alert_stock()
            time.sleep(15)
def main_thread():
    global my_watchlist
    my_watchlist = Listed_watchlist()
    threading1 = threading.Thread(target=my_watchlist.updateAnd_alert)
    threading1.daemon= True
    threading1.start()
                    
def main():
    engine = pyttsx3.init()
    tprint("STOCKSZ NOTIFIER", font="cybermedium")
    Interface()
def Interface():
    global my_watchlist
    my_watchlist = Listed_watchlist()
    main_thread()
    valid_menus= f"Commands: {'INFO', 'EDIT', 'LTP', 'EXIT'}"
    while True:
        print(valid_menus)
        req = input("_ ").upper()
        if not req in valid_menus:
            print(f"'{req}' is not a valid command")
        else:
            Req_handler(req)

def Req_handler(req, stock= None):
    if req == "EXIT":
        return sys.exit("Shutting script")
    if req == "INFO":
        try:
            if stock != None:
                info_data= yf.Ticker(stock).info
                sys.exit(info_data)
            else:
                print("Type the stock symbol for info")
                info_stock= input("_ ").upper()
                info_data= yf.Ticker(info_stock).info
            if info_stock == "BACK":
                return
            elif info_stock == "EXIT":
                sys.exit("Shutting script")
            if info_data or (info_stock== "BACK" or info_stock== "EXIT"):
                if info_stock== "BACK":
                    return
                elif info_stock== "EXIT":
                    sys.exit("Shutting script")
                print(info_data)
            else:
                raise ValueError
        except ValueError:
            print("Invalid symbol try again")
            return
    if req == "LTP":
        my_watchlist.update_stocks()
        my_watchlist.watchlist_ltp()
    if req == "EDIT":
        watchlist_modify()

def watchlist_modify():
    if __name__ == "__main__":
        my_watchlist = Listed_watchlist()
    print("Modifying watchlist")
    watchlist_edit_menus= f"Commands: {"ADD", "ALERT", "REMOVE", "LTP", "BACK", "EXIT"}"
    while True:
        print(watchlist_edit_menus)
        w_modify_req= input("_").upper()
        if w_modify_req == "EXIT":
            sys.exit("Shutting script")
        elif w_modify_req == "ADD":
            my_watchlist.Add_stocks()
        elif w_modify_req == "LTP":
            my_watchlist.watchlist_ltp()
        elif w_modify_req == "ALERT":
            my_watchlist.stockAlert()
        elif w_modify_req == "REMOVE":
            my_watchlist.Remove_stocks()
        elif w_modify_req == "BACK":
            return
        else:
            print(f"'{w_modify_req}' is not a valid command")
            
def Sys_handler(arg):
    global my_watchlist
    my_watchlist = Listed_watchlist()
    while True:
        if len(sys.argv)== 2:
            if sys.argv[1].upper() == "LTP":
                my_watchlist.update_stocks()
                my_watchlist.watchlist_ltp()
                break
            else:
                return False
            
        elif len(sys.argv)== 3:
            if sys.argv[1].upper() == "ADD":
                stock= sys.argv[2].upper()
                check=my_watchlist.Add_check(stock)
                if check:
                    yinfo= yf.Ticker(stock).info
                    my_watchlist.watchlist_edit(yinfo)
                    print(f"Added {stock} to the watchlist")
                    break
            if sys.argv[1].upper() == "REMOVE":
                stock= sys.argv[2].upper()
                check=my_watchlist.Remove_stocks(stock)
                if check:
                    print(f"Removed {stock} from the watchlist")
                    break
        else:
            sys.exit("")

if __name__ == "__main__":
    sys_menu = {"EDIT", "LTP", "INFO", "ADD", "REMOVE"}
    while True:
        if len(sys.argv) != 1:
            if len(sys.argv) == 3 and sys.argv[1].upper() in {"ADD", "REMOVE", "INFO"}:
                if sys.argv[1].upper() == "INFO":
                    req= sys.argv[1].upper()
                    stock= sys.argv[2].upper()
                    Req_handler(req, stock)
                else:
                    Sys_handler(sys.argv)
                sys.exit(f"available commands: {sys_menu}")
            elif len(sys.argv) == 2 and sys.argv[1].upper() in {"LTP"}:
                Sys_handler(sys.argv)
                sys.exit(f"available commands: {sys_menu}")
            elif len(sys.argv) == 2 and sys.argv[1].upper() in {"EDIT"}:
                Req_handler(sys.argv[1].upper())
            else:
                print("Unknown command")
                sys.exit(f"available commands: {sys_menu}")
        else:
            main()
