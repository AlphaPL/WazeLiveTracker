# WazeLiveTracker


This script does a very simple thing - it scrapes accident data for specified post codes from Waze. You specify postcodes in postcodes.csv . You set two environment variables CHAT_ID - id of telegram channel - and BOT_API_KEY - api key for a telegram bot. Once you do it and run the script once an accident occurs in the vicinity of the post codes you will get an alert about it on the specified Telegram channel.

Typical alert on Telegram

![Alt text](/alertontelegram.png?raw=true "Optional Title")
