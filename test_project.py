import pytest
import sys
import yfinance as yf
import pandas as pd
import os
import threading
import winsound
import time
from art import *
import cowsay
from unittest.mock import patch
import pyttsx3
from project import Req_handler,Sys_handler, Listed_watchlist

def main():
    test_Req_handler()
    test_sys_argument()
def test_Req_handler():
    with pytest.raises(SystemExit):
        Req_handler("EXIT")
    assert Req_handler("BACK") == None



@pytest.fixture
def my_watchlist():
    return Listed_watchlist()
def test_sys_argument():
    assert Sys_handler("LhTP") == False
    assert Sys_handler("ADD")== False
    assert Sys_handler("ADD")== False
    with pytest.raises(SystemExit):
        sys.argv=["","ADD", "T"]
        Sys_handler(sys.argv)
    with pytest.raises(SystemExit):
        sys.argv=["","REMOVE", "T"]
        Sys_handler(sys.argv)

@pytest.fixture
def my_watchlist():
    return Listed_watchlist()
def test_watchlist_class():
    my_watchlist = Listed_watchlist()
    stock =yf.Ticker("T").info
    assert my_watchlist.watchlist_edit(stock)== True
    