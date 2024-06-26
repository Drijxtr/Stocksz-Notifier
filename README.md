# Stocks Notifier
#### Video Demo: https://youtu.be/4bFws57iwxA
#### Description

Stocks Notifier is a simple Python script that tracks your stocks and notifies you when they reach your desired price.

## Features

- **Updates data every 15s:** Stay up-to-date with the latest stock prices using Yahoo Finance.
- **Custom Alerts:** Set alerts for price changes based on your conditions.
- **Watchlist Management:** Easily add, edit, and remove stocks from your watchlist.
- **Notifications:** Get notified with sound and text-to-speech alerts.
- **Command Line Interface:** Simple commands to interact with the tool.

## Getting Started

To get started, you'll need Python and a few libraries. Install them by running:

```sh
pip install yfinance pandas art cowsay pyttsx3
```



## Command Line Interface (CLI) Commands

##### ADD: Add a new stock to your watchlist.
```sh
location/project.py ADD NVDA
```
##### REMOVE: Remove a stock from your watchlist.
```sh
location/project.py REMOVE NVDA
```
##### LTP: Prints the latest prices for your watchlist stocks.
```sh
location/project.py LTP
```
##### INFO: Get detailed information about a stock.
```sh
location/project.py INFO
```
##### EDIT: Directly opens the watchlist editor to add/remove stocks or set alerts.  
```sh
location/project.py EDIT
```


## In-Script Menu Options

##### ADD: Adds a new stock to your watchlist.
##### REMOVE: Removes a stock from your watchlist.
##### ALERT: Sets a price alert for a stock.
##### INFO: Get detailed information about a stock.
##### EDIT: Directly opens the watchlist editor to add/remove stocks or set alerts.  
##### LTP: Shows the latest prices for your watchlist stocks.



## Note to Users and Contributors

This is my first project, and I'm eager to learn and improve. If you have any suggestions, feedback, or would like to contribute to the project, please feel free to open an issue or submit a pull request. Your insights are highly valued!

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

