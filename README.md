# Stocks Notifier

## Description

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

## Command lines:

INFO: Get detailed information about a specific stock.
EDIT: Open the watchlist editor to add/remove stocks or set alerts.
LTP: Display the latest prices for your watchlist stocks.
EXIT: Exit the application.
Edit Watchlist Commands:

ADD: Add a new stock to your watchlist.
REMOVE: Remove a stock from your watchlist.
ALERT: Set a price alert for a stock.
LTP: Show the latest prices for your watchlist stocks.
BACK: Return to the main menu.
EXIT: Exit the application.
Example Usage
Here's how you can use Stocks Notifier:

Add a Stock:

Type ADD and enter the stock symbol (like AAPL for Apple).

Set an Alert:

Type ALERT, enter the stock symbol, and then set your alert condition (>, <, >=, <=, ==) and price.

Check Latest Prices:

Type LTP to see the current prices of all stocks in your watchlist.

Remove a Stock:

Type REMOVE and enter the stock symbol you want to remove.

Customizing Alerts
Want to customize the alert sound? Just replace the alert_sound.wav file in the project directory. Make sure the new file has the same name and format.
