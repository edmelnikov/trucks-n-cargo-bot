# trucks-n-cargo-bot

This is a telegram bot that searches for and prints out listings of trucks from https://trucks.ati.su/ or listings of cargo from https://loads.ati.su/ depending on user's query.

The bot interface is implemented using python-telegram-bot (https://github.com/python-telegram-bot/python-telegram-bot) by [@katyamalysheva](https://github.com/katyamalysheva).

The backend of the bot that provides the listing data is implemented with Selenium WebDriver by me. Basically, it scrapes the page with listings and retrieves listing data like departure and arrival city, distance, weight, etc.

The bot was left unfinished since testing under high load (10-15 people making queries at a time) had shown that using Selenium WebDriver to scrape a page imposes high overhead. For each query 
a new instance of Google Chrome has to be launched which is far from beeing fast or optimal. 
