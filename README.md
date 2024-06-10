# Currency Monitoring 

The python script currencyMonitor.py is used to get the currency exchange details between two countries based on the country codes 
defined in https://en.wikipedia.org/wiki/ISO_4217. This script uses the api given by https://www.exchangerate-api.com/. The api key is free for all once you
register with your email address.
(Caveats https://www.exchangerate-api.com/ updates the exchange rate every day once)

The script currencyMonitor.py uses the api https://www.exchangerate-api.com/ to get the exchange rate between two currencies at a frequency defined by 
the user for a duration that has also been requested by the user while running the script. The script also logs to a log file every 60 seconds
once the average of the exchange rates.

## How to run the script
Support python version : 3.9.6
python3 currencyMonitor.py [-h] [-f LOG_FILE] [-b BASE_CURRENCY] [-d DEST_CURRENCY] [-a API_KEY] [--sample_rate SAMPLE_RATE] [--duration DURATION]

-f is the log file where you want to store the logs
-b is the base currency name from you want to monitor the exchange value (should follow https://en.wikipedia.org/wiki/ISO_4217 standard)
-f is the destination currency name to which you want to exchange (should follow https://en.wikipedia.org/wiki/ISO_4217 standard)
-a is the api key that you have obtained from https://www.exchangerate-api.com/
--sample_rate is the frequency at which you want to get the exchange values
--duration is the duration you want the program to monitor the exchange rate